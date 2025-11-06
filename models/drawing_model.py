from __future__ import annotations
from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Field, Relationship
from models.base import Base
from models.registry import register_model


@register_model
class Drawing(Base, table=True):
    __tablename__ = "drawing"

    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str = Field(nullable=False)
    file_path: str = Field(nullable=False)
    file_type: Optional[str] = Field(default=None)
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    uploader_id: Optional[int] = Field(default=None, foreign_key="user.id")
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")

    uploader: "User" = Relationship(back_populates="drawings", sa_relationship="User")
    project: "Project" = Relationship(back_populates="drawings", sa_relationship="Project")
    estimations: List["Estimation"] = Relationship(back_populates="drawing", sa_relationship="Estimation")
