from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from . import schemas, service

router = APIRouter(prefix="/sentiment", tags=["Sentiment AI"])

@router.post("/analysis", response_model=schemas.SentimentResponse)
async def sentiment_analysis(req: schemas.SentimentRequest, db: AsyncSession = Depends(get_db)):
    result = await service.analyze_sentiment(req.text)
    # 예: DB에 임베딩 저장도 가능
    # await service.save_embedding(db, req.article_id, [0.1]*1536)
    return result

@router.post("/batch")
async def batch_analysis(req: schemas.BatchRequest):
    # 간단 예: 비동기 호출 생략
    results = []
    for item in req.texts:
        res = await service.analyze_sentiment(item.text)
        results.append({
            "id": item.id,
            "sentiment_score": res["sentiment_score"],
            "sentiment_label": res["sentiment_label"],
            "confidence": res["confidence"]
        })
    return {"results": results, "total_processed": len(results)}
