from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class MealCreate(BaseModel):
    title: str
    description: Optional[str] = None
    calories: Optional[int] = None


class MealOut(MealCreate):
    id: int
    timestamp: Optional[datetime] = None


class MealAnalyzeRequest(BaseModel):
    meals: Optional[str] = None
    goal: Optional[str] = None


class BMIRequest(BaseModel):
    weight: float = Field(..., gt=0)
    height_cm: float = Field(..., gt=0)


class ChatRequest(BaseModel):
    messages: List[str]
    topic: Optional[str] = Field(
        default="general",
        description="Intended topic for the chat request, e.g., 'nutrition' or 'fitness'.",
    )


class RecommendResponse(BaseModel):
    """Response model for the /recommend endpoint"""

    nutrition: str
    supplements: List[str]

