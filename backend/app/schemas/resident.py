from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ResidentBase(BaseModel):
    full_name: str
    period_start: Optional[str] = None
    period_end: Optional[str] = None
    role: Optional[str] = None


class ResidentCreate(ResidentBase):
    location_id: UUID
    user_id: Optional[UUID] = None


class ResidentResponse(ResidentBase):
    id: UUID
    location_id: UUID
    user_id: Optional[UUID] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
