from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DrawingCreate(BaseModel):
    filename:str
    file_type:Optional[str]=None
    
    
class DrawingRead(BaseModel):
    id:int
    filename:str
    file_path: str
    uploaded_at:datetime
    upload_id: int
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }