import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv # Used to load environment variables from .env file

# Load environment variables from .env file
load_dotenv()

# Retrieve the DATABASE_URL from environment variables
""" Transaction pooler"""
DATABASE_URL="postgresql+asyncpg://postgres.[프로젝트주소]:[db비밀번호]@aws-0-ap-northeast-2.pooler.supabase.com:6543/postgres"

# Raise an error if DATABASE_URL is not set, as it's critical for database connection
if not DATABASE_URL:
    raise ValueError("DATABASE_URL 환경변수가 설정되지 않았습니다. .env 파일을 확인해주세요.")

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=20,
    max_overflow=0,
    connect_args={"statement_cache_size": 0}  # !Disable prepared statement cache
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()