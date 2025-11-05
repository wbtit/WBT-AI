from sqlmodel import SQLModel, Field
from typing import Optional,List
from datetime import datetime, timezone
import uuid
from sqlmodel import Relationship



class User(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    public_id: str = Field(default_factory=lambda:str(uuid.uuid4()),index=True,unique=True)
    email:str= Field(index=True,unique=True,nullable=False)
    hashed_password:str
    username:str= Field(index=True,unique=True,nullable=False)
    is_active:bool=Field(default=True)
    role:str=Field(default="ESTIMATOR")  # Roles: ADMIN, ESTIMATOR, USER
    created_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
    drawings: List["Drawing"]= Relationship(back_populates="uploader")
    
    
#This is imported at the bottom to avoid circular imports with drawing_model
from models.drawing_model import Drawing
    