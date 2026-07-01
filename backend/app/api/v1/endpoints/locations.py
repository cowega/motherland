from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from geoalchemy2.elements import WKTElement

from app.db.session import get_db
from app.models.location import Location, LocationType
from app.models.resident import Resident
from app.models.user import User
from app.schemas.location import LocationCreate, LocationResponse
from app.api.deps import get_current_user
from app.exceptions import (
    LocationNotFoundException,
    CoordinatesRequiredException,
    ParentLocationRequiredException,
    InvalidStreetParentException,
    InvalidBuildingParentException,
    InvalidRoomParentException,
    InvalidSettlementParentException
)

router = APIRouter()


@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
async def create_location(
    location_in: LocationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Location:
    if location_in.type in [LocationType.settlement, LocationType.building]:
        if not location_in.coordinates:
            raise CoordinatesRequiredException()

    if location_in.type != LocationType.settlement:
        if location_in.parent_id is None:
            raise ParentLocationRequiredException()

    if location_in.parent_id is not None:
        parent_query = select(Location).where(Location.id == location_in.parent_id)
        parent_result = await db.execute(parent_query)
        parent = parent_result.scalars().first()
        if not parent:
            raise LocationNotFoundException()

        if location_in.type == LocationType.street and parent.type != LocationType.settlement:
            raise InvalidStreetParentException()
        elif location_in.type == LocationType.building and parent.type != LocationType.street:
            raise InvalidBuildingParentException()
        elif location_in.type == LocationType.room and parent.type != LocationType.building:
            raise InvalidRoomParentException()
        elif location_in.type == LocationType.settlement and parent.type != LocationType.settlement:
            raise InvalidSettlementParentException()

    db_location = Location(
        type=location_in.type,
        name=location_in.name,
        parent_id=location_in.parent_id,
        created_by=current_user.id
    )
    if location_in.coordinates:
        db_location.coordinates = WKTElement(
            f"POINT({location_in.coordinates.longitude} {location_in.coordinates.latitude})",
            srid=4326
        )

    db.add(db_location)
    await db.flush()

    if location_in.type in [LocationType.settlement, LocationType.building]:
        db_resident = Resident(
            location_id=db_location.id,
            user_id=current_user.id,
            full_name=current_user.full_name,
            period_start=location_in.period_start,
            period_end=location_in.period_end,
            role=location_in.role
        )
        db.add(db_resident)

    await db.commit()
    await db.refresh(db_location)
    return db_location


@router.get("/", response_model=List[LocationResponse])
async def list_locations(
    type: Optional[LocationType] = None,
    parent_id: Optional[UUID] = None,
    root_only: bool = False,
    db: AsyncSession = Depends(get_db)
) -> List[Location]:
    query = select(Location)
    if type is not None:
        query = query.where(Location.type == type)
    if parent_id is not None:
        query = query.where(Location.parent_id == parent_id)
    elif root_only:
        query = query.where(Location.parent_id.is_(None))

    query = query.order_by(Location.name)
    result = await db.execute(query)
    return list(result.scalars().all())


@router.get("/{id}", response_model=LocationResponse)
async def get_location(
    id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Location:
    query = select(Location).where(Location.id == id)
    result = await db.execute(query)
    location = result.scalars().first()
    if not location:
        raise LocationNotFoundException()
    return location
