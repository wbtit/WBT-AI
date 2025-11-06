from __future__ import annotations
from typing import Optional, List
from datetime import datetime, timezone
import uuid
from sqlmodel import Field, Relationship
from models.base import Base
from models.registry import register_model

@register_model
class User(Base, table=True):
    __tablename__ = "user"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    public_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    username: str = Field(unique=True, nullable=False)
    is_active: bool = Field(default=True)
    role: str = Field(default="ESTIMATOR")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Define relationships with string literals
    drawings: List["Drawing"] = Relationship(back_populates="uploader", sa_relationship="Drawing")
    projects: List["Project"] = Relationship(back_populates="owner", sa_relationship="Project")
