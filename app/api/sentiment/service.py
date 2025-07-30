from sqlalchemy.ext.asyncio import AsyncSession
from app.db import models
from datetime import datetime

async def analyze_sentiment(text: str) -> dict:
    # TODO: 실제 모델 호출
    return {
        "sentiment_score": 0.8,
        "sentiment_label": "긍정",
        "confidence": 0.95,
        "model_version": "sentiment_v1.0",
        "inference_time_ms": 800,
        "detailed_scores": {"positive": 0.85, "neutral": 0.10, "negative": 0.05}
    }

async def save_embedding(db: AsyncSession, article_id: str, embedding: list):
    await db.execute(
        """
        UPDATE original_articles
        SET embedding = :embedding
        WHERE id = :article_id
        """,
        {"embedding": embedding, "article_id": article_id}
    )
    await db.commit()

async def similarity_search(db: AsyncSession, embedding: list, limit: int = 5):
    # pgvector 유사도 검색
    result = await db.execute(
        """
        SELECT id, title, content, 1 - (embedding <=> :embedding) AS similarity
        FROM original_articles
        ORDER BY embedding <=> :embedding
        LIMIT :limit
        """,
        {"embedding": embedding, "limit": limit}
    )
    return result.fetchall()
