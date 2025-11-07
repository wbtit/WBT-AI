from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Projectcreate(BaseModel):
    name:str
    description:Optional[str]=None
    
class Projectread(BaseModel):
    id:Optional[int]
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    owner_id: int
    
    class Config:
        orm_mode = True
    
class Projectupdate(BaseModel):
    name:Optional[str]=None
    description:Optional[str]=None  
    owner_id:Optional[int]=None

class Projectlist(BaseModel):
    id:int
    name:str
    description:Optional[str]=None
    created_at:datetime
    updated_at:datetime
    owner_id:int
    
    class Config:
        orm_mode = True 

class Projectdelete(BaseModel):
    id:int
    
    class Config:
        orm_mode = True