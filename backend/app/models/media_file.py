import uuid
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlalchemy import String, DateTime, ForeignKey, Integer, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
import enum


class MediaType(str, enum.Enum):
    photo = "photo"
    video = "video"


class MediaFile(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    memory_id: Mapped[UUID] = mapped_column(ForeignKey("memories.id", ondelete="CASCADE"), nullable=False)
    uploaded_by: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    file_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    file_type: Mapped[MediaType] = mapped_column(SqlEnum(MediaType), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    original_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    memory: Mapped["Memory"] = relationship(back_populates="media_files")
    uploader: Mapped[Optional["User"]] = relationship(back_populates="media_files")
    photo_tags: Mapped[List["PhotoTag"]] = relationship(back_populates="media_file", cascade="all, delete-orphan")
