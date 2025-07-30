# original_articles 테이블 매핑, embedding 포함

from sqlalchemy import Column, String, Text, TIMESTAMP, ARRAY
from sqlalchemy.dialects.postgresql import VECTOR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OriginalArticle(Base):
    __tablename__ = "original_articles"

    id = Column(String, primary_key=True, index=True)
    url = Column(Text, nullable=True)
    category = Column(Text, nullable=True)
    published_at = Column(TIMESTAMP, nullable=True)
    title = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    thumbnail_url = Column(Text, nullable=True)
    reporter = Column(Text, nullable=True)
    press = Column(Text, nullable=True)
    keywords = Column(ARRAY(Text), nullable=True)
    scraped_at = Column(TIMESTAMP, nullable=True)
    embedding = Column(VECTOR(1536), nullable=True)  # 예: OpenAI 임베딩 차원 1536
