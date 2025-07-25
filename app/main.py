from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.user.router import router as user_router
import asyncio # Required for asyncio.sleep in retry logic
import sys

MAX_DB_RETRIES = 5  # Adjust as needed
RETRY_DB_DELAY = 5  # Seconds to wait between retries

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for startup and shutdown events.
    Handles database connection and table creation with retry logic.
    """
    # --- Startup Logic ---
    connected_to_db = False
    for i in range(MAX_DB_RETRIES):
        try:
            print(f"Attempting to connect to database and create tables (Attempt {i+1}/{MAX_DB_RETRIES})...")
            # Attempt to connect to the database and run migrations
            print(engine)
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✅ 데이터베이스 테이블이 성공적으로 생성되었습니다.")
            connected_to_db = True
            break  # Exit loop if connection and table creation are successful
        except Exception as e:
            print(f"❌ 데이터베이스 연결 또는 테이블 생성 실패: {e}")
            if i < MAX_DB_RETRIES - 1:
                print(f"재시도 중... ({RETRY_DB_DELAY}초 후)")
                await asyncio.sleep(RETRY_DB_DELAY)  # Wait before retrying
            else:
                print("🚨 모든 재시도 실패. 데이터베이스에 연결할 수 없습니다. 애플리케이션을 종료합니다.")
                raise  # Re-raise the exception to prevent the app from starting

    if not connected_to_db:
        print("🚨 FastAPI 애플리케이션이 데이터베이스 연결 없이 시작될 수 없습니다. 확인해주세요.")
        sys.exit(1)  # Force exit if connection failss

    yield  # Application runs after successful startup

    # --- Shutdown Logic ---
    print("❌ 데이터베이스 연결을 종료합니다.")
    await engine.dispose()  # Dispose of the database engine connections
    print("❌ 데이터베이스 연결이 성공적으로 종료되었습니다.")

# FastAPI 앱 생성
app = FastAPI(
    title="User API",
    description="FastAPI + Supabase PostgreSQL",
    version="1.0.0",
    lifespan=lifespan # Register the lifespan context manager
)

# 라우터 등록
app.include_router(user_router, prefix="/User", tags=["user"])

@app.get("/")
async def root():
    """
    Root endpoint for the API.
    """
    return {"message": "User API with Supabase PostgreSQL"}

#uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI application using uvicorn
    # 'reload=True' is useful for development, automatically reloads on code changes
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
