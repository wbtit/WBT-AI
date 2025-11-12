from __future__ import annotations
from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Field, Relationship
from models.base import Base
from models.registry import register_model

@register_model
class Project(Base, table=True):
    __tablename__ = "project"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    owner_id: int = Field(foreign_key="user.id")

    drawings: List["Drawing"] = Relationship(back_populates="project", sa_relationship="Drawing")
    owner: "User" = Relationship(back_populates="projects", sa_relationship="User")

@register_model
class Estimation(Base, table=True):
    __tablename__ = "estimation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    drawing_id: int = Field(foreign_key="drawing.id")
    category: str = Field(nullable=False)
    width: Optional[float] = Field(default=None, nullable=True)
    height: Optional[float] = Field(default=None, nullable=True)
    material: Optional[str] = Field(default="Unknown", nullable=True)
    cost: Optional[float] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    drawing: "Drawing" = Relationship(back_populates="estimations", sa_relationship="Drawing")
