from datetime import datetime
from typing import Optional, Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator
from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape

from app.models.location import LocationType


class PointSchema(BaseModel):
    latitude: float
    longitude: float


class LocationBase(BaseModel):
    name: str
    type: LocationType


class LocationCreate(LocationBase):
    parent_id: Optional[UUID] = None
    coordinates: Optional[PointSchema] = None
    period_start: Optional[str] = None
    period_end: Optional[str] = None
    role: Optional[str] = None


class LocationResponse(LocationBase):
    id: UUID
    parent_id: Optional[UUID] = None
    created_by: Optional[UUID] = None
    coordinates: Optional[PointSchema] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("coordinates", mode="before")
    @classmethod
    def parse_coordinates(cls, value: Any) -> Optional[PointSchema]:
        if value is None:
            return None
        if isinstance(value, WKBElement):
            try:
                shape = to_shape(value)
                return PointSchema(latitude=shape.y, longitude=shape.x)
            except Exception:
                return None
        if isinstance(value, dict):
            return PointSchema(**value)
        return value
