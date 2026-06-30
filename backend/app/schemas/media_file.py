from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.models.media_file import MediaType


class MediaFileBase(BaseModel):
    file_url: str
    file_type: MediaType
    size_bytes: int
    duration_seconds: Optional[int] = None
    original_date: Optional[datetime] = None


class MediaFileCreate(MediaFileBase):
    memory_id: UUID


class MediaFileResponse(MediaFileBase):
    id: UUID
    memory_id: UUID
    uploaded_by: Optional[UUID] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
