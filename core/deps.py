from fastapi import Depends, HTTPException, status
from jose import JWTError
from fastapi.security import APIKeyHeader
from sqlmodel import Session, select
from db.session import get_session
from models.user_model import User
from core.security import decode_token

api_key_scheme = APIKeyHeader(name="Authorization", auto_error=False)


def get_current_user(token: str = Depends(api_key_scheme), session: Session = Depends(get_session)) -> User:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    parts = token.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header format. Expected 'Bearer <token>'")

    payload = decode_token(parts[1])
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    public_id = payload.get("sub")
    if not public_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    user = session.exec(select(User).where(User.public_id == public_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user
