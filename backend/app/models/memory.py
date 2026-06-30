import uuid
from datetime import datetime, date
from typing import Optional, List
from uuid import UUID
from sqlalchemy import String, DateTime, ForeignKey, Date, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
import enum


class PrivacyType(str, enum.Enum):
    public = "public"
    private = "private"
    family = "family"


class Memory(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    location_id: Mapped[UUID] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    text_content: Mapped[str] = mapped_column(String, nullable=False)
    
    privacy: Mapped[PrivacyType] = mapped_column(SqlEnum(PrivacyType), default=PrivacyType.public, nullable=False)
    family_token: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True, nullable=True)
    
    event_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author: Mapped["User"] = relationship(back_populates="memories")
    location: Mapped["Location"] = relationship(back_populates="memories")
    media_files: Mapped[List["MediaFile"]] = relationship(back_populates="memory", cascade="all, delete-orphan")
