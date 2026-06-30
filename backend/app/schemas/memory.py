from datetime import datetime, date
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.models.memory import PrivacyType
from app.schemas.media_file import MediaFileResponse


class MemoryBase(BaseModel):
    title: str
    text_content: str
    privacy: PrivacyType = PrivacyType.public
    event_date: Optional[date] = None


class MemoryCreate(MemoryBase):
    location_id: UUID


class MemoryResponse(MemoryBase):
    id: UUID
    user_id: UUID
    location_id: UUID
    family_token: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    media_files: List[MediaFileResponse] = []

    model_config = ConfigDict(from_attributes=True)
