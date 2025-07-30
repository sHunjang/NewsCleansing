import sys
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.session import engine
from app.db.models import Base  # models.py 에 Base 선언되어 있다고 가정
from app.api.sentiment.router import router as sentiment_router

# DB 연결 설정
MAX_DB_RETRIES = 5
RETRY_DB_DELAY = 2  # 초

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan: startup & shutdown
    - Startup: DB 연결 및 테이블 생성 (재시도 포함)
    - Shutdown: DB 연결 해제
    """
    for attempt in range(1, MAX_DB_RETRIES + 1):
        try:
            print(f"🚀 [Startup] Connecting to DB & creating tables (Attempt {attempt}/{MAX_DB_RETRIES})...")
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✅ DB 연결 및 테이블 생성 완료!")
            break
        except Exception as e:
            print(f"❌ DB 연결 실패: {e}")
            if attempt < MAX_DB_RETRIES:
                print(f"⏳ {RETRY_DB_DELAY}초 후 재시도...")
                await asyncio.sleep(RETRY_DB_DELAY)
            else:
                print("🚨 모든 재시도 실패. 애플리케이션을 종료합니다.")
                sys.exit(1)
    yield
    print("🛑 [Shutdown] Closing DB engine...")
    await engine.dispose()
    print("✅ DB engine closed.")

# FastAPI 앱 생성
app = FastAPI(
    title="News Cleansing Model API",
    description="Sentiment analysis + Supabase PostgreSQL + FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# 라우터 등록
app.include_router(sentiment_router, prefix="/sentiment", tags=["Sentiment"])

@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {"message": "Welcome to News Cleansing API with Supabase PostgreSQL"}

# uvicorn 실행 , uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8004, reload=True)
