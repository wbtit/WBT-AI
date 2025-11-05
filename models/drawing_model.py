from sqlmodel import SQLModel,Field,Relationship
from typing import Optional
from datetime import datetime, timezone

from models.user_model import User

class Drawing(SQLModel,table=True):
    id:int= Field(default=None,primary_key=True)
    filename:str
    file_path:str
    file_type:Optional[str]=None
    uploaded_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
    created_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
    #Relationships
    uploader:Optional["User"]= Relationship(back_populates="drawings")