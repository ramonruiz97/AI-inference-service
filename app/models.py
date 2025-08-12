from pydantic import BaseModel, Field
from typing import List, Optional


#Data models to validate certain data-structures ~ similar to Serializers

class PredictIn(BaseModel):
    #... Means mandatory
    texts: List[str] = Field(..., min_length=1, max_length=128)
    #Optional number between [1, 5]
    top_k: Optional[int] = Field(1, ge=1, le=5)

class Prediction(BaseModel):
    label: str
    score: float

class PredictOut(BaseModel):
    results: List[List[Prediction]]
    processing_ms: int