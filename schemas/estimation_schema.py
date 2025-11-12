from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EstimationBase(BaseModel):
    category: str
    width: float
    height: float
    material: str
    cost: Optional[float] = None

class EstimationCreate(EstimationBase):
    drawing_id: int

class EstimationRead(EstimationBase):
    id: int
    drawing_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }