import uuid
from datetime import datetime
from uuid import UUID
from sqlalchemy import DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class PhotoTag(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    media_file_id: Mapped[UUID] = mapped_column(ForeignKey("media_files.id", ondelete="CASCADE"), nullable=False)
    resident_id: Mapped[UUID] = mapped_column(ForeignKey("residents.id", ondelete="CASCADE"), nullable=False)
    
    x_percent: Mapped[float] = mapped_column(Float, nullable=False)
    y_percent: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    media_file: Mapped["MediaFile"] = relationship(back_populates="photo_tags")
    resident: Mapped["Resident"] = relationship(back_populates="photo_tags")
