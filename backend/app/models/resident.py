import uuid
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Resident(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    location_id: Mapped[UUID] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    period_start: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    period_end: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    location: Mapped["Location"] = relationship(back_populates="residents")
    user: Mapped[Optional["User"]] = relationship(back_populates="residents")
    photo_tags: Mapped[List["PhotoTag"]] = relationship(back_populates="resident", cascade="all, delete-orphan")
