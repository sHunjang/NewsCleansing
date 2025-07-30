from pydantic import BaseModel
from typing import List, Dict

class SentimentRequest(BaseModel):
    text: str
    article_id: str

class SentimentResponse(BaseModel):
    sentiment_score: float
    sentiment_label: str
    confidence: float
    model_version: str
    inference_time_ms: int
    detailed_scores: Dict[str, float]

class BatchItem(BaseModel):
    id: str
    text: str

class BatchRequest(BaseModel):
    texts: List[BatchItem]

class BatchResult(BaseModel):
    id: str
    sentiment_score: float
    sentiment_label: str
    confidence: float
