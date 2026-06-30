import uuid
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class User(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    locations: Mapped[List["Location"]] = relationship(back_populates="creator", cascade="all, delete-orphan")
    memories: Mapped[List["Memory"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    media_files: Mapped[List["MediaFile"]] = relationship(back_populates="uploader", cascade="all, delete-orphan")
    residents: Mapped[List["Resident"]] = relationship(back_populates="user", cascade="all, delete-orphan")
