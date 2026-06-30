from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class PhotoTagBase(BaseModel):
    x_percent: float
    y_percent: float


class PhotoTagCreate(PhotoTagBase):
    media_file_id: UUID
    resident_id: UUID


class PhotoTagResponse(PhotoTagBase):
    id: UUID
    media_file_id: UUID
    resident_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
