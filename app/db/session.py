import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL 환경변수가 설정되지 않았습니다. .env 파일을 확인해주세요.")

# Create SQLAlchemy async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=20,           # 최대 연결 풀 크기
    max_overflow=0,         # 추가 연결 허용 안 함
    connect_args={"statement_cache_size": 0}  # PgBouncer 대비 prepared statement cache 비활성화
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency: FastAPI에서 주입용
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
