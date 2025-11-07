from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user_schema import UserRead,UserCreate,UserLogin
from sqlmodel import Session, select
from db.session import get_session
from models.user_model import User 
from core.security import hash_password,verify_password,create_access_token
from core.deps import get_current_user
import logging

router = APIRouter()

@router.post("/register",response_model=UserRead)
def register_user(user_data:UserCreate,session:Session = Depends(get_session)):
    user_exists = session.exec(select(User).where(User.email==user_data.email)).first()
    if user_exists:
        raise HTTPException(status_code=400,detail="Email already registered")
    
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        username=user_data.username
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.post("/login")
def login_user(user_data:UserLogin,session:Session= Depends(get_session)):
    user = session.exec(select(User).where(User.email==user_data.email)).first()
    if not user or not verify_password(user_data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    
    token = create_access_token({"sub": user.public_id})
    return {"access_token": token,"token_type":"Bearer"}


@router.get("/me",response_model=UserRead)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    logging.info(f"Fetching info for user: {current_user.email}")
    return current_user

@router.get("/users",response_model=List[UserRead])
def list_users(session:Session=Depends(get_session)):
    users = session.exec(select(User)).all()
    return users
