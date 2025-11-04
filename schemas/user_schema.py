from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    
class UserRead(BaseModel):
    id: int
    public_id: str
    email: EmailStr
    username: str
    is_active: bool
    role: str
    created_at: str
    updated_at: str
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None
    
    class Config:
        orm_mode = True