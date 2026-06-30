import uuid
from datetime import datetime
from typing import Optional, List, Any
from uuid import UUID
from sqlalchemy import String, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry

from app.db import Base
import enum


class LocationType(str, enum.Enum):
    settlement = "settlement"
    street = "street"
    building = "building"
    room = "room"


class Location(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    type: Mapped[LocationType] = mapped_column(SqlEnum(LocationType), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    coordinates: Mapped[Optional[Any]] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True), 
        nullable=True
    )
    
    parent_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"), nullable=True)
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    creator: Mapped[Optional["User"]] = relationship(back_populates="locations")
    
    parent: Mapped[Optional["Location"]] = relationship(
        "Location", 
        remote_side=[id], 
        back_populates="children"
    )
    children: Mapped[List["Location"]] = relationship(
        "Location", 
        back_populates="parent", 
        cascade="all, delete-orphan"
    )

    memories: Mapped[List["Memory"]] = relationship(back_populates="location", cascade="all, delete-orphan")
    residents: Mapped[List["Resident"]] = relationship(back_populates="location", cascade="all, delete-orphan")
