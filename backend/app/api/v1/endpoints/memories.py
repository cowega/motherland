from typing import List, Optional
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.memory import Memory, PrivacyType
from app.models.location import Location
from app.models.user import User
from app.schemas.memory import MemoryCreate, MemoryResponse
from app.api.deps import get_current_user
from app.core.security import decode_access_token
from app.exceptions import MemoryNotFoundException, LocationNotFoundException, AccessDeniedException

router = APIRouter()

oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        if not payload:
            return None
        user_id = payload.get("sub")
        if not user_id:
            return None
        # Проверяем формат UUID, чтобы не упасть на запросе к БД
        UUID(str(user_id))
    except (ValueError, TypeError, Exception):
        return None

    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalars().first()


@router.post("/", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
async def create_memory(
    memory_in: MemoryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Memory:
    location_query = select(Location).where(Location.id == memory_in.location_id)
    location_result = await db.execute(location_query)
    location_exists = location_result.scalars().first()
    if not location_exists:
        raise LocationNotFoundException()

    family_token = None
    if memory_in.privacy == PrivacyType.family:
        family_token = str(uuid4())

    db_memory = Memory(
        user_id=current_user.id,
        location_id=memory_in.location_id,
        title=memory_in.title,
        text_content=memory_in.text_content,
        privacy=memory_in.privacy,
        family_token=family_token,
        event_date=memory_in.event_date
    )

    db.add(db_memory)
    await db.commit()

    query = select(Memory).where(Memory.id == db_memory.id).options(selectinload(Memory.media_files))
    res = await db.execute(query)
    return res.scalars().first()


@router.get("/", response_model=List[MemoryResponse])
async def list_memories(
    location_id: UUID,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
) -> List[Memory]:
    query = select(Memory).where(Memory.location_id == location_id).options(selectinload(Memory.media_files))
    if current_user:
        query = query.where(
            (Memory.privacy == PrivacyType.public) |
            (Memory.user_id == current_user.id)
        )
    else:
        query = query.where(Memory.privacy == PrivacyType.public)

    query = query.order_by(Memory.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


@router.get("/{id}", response_model=MemoryResponse)
async def get_memory(
    id: UUID,
    token: Optional[str] = None,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
) -> Memory:
    query = select(Memory).where(Memory.id == id).options(selectinload(Memory.media_files))
    result = await db.execute(query)
    memory = result.scalars().first()
    if not memory:
        raise MemoryNotFoundException()

    if memory.privacy == PrivacyType.public:
        return memory

    if current_user and memory.user_id == current_user.id:
        return memory

    if memory.privacy == PrivacyType.family and token and memory.family_token and memory.family_token == token:
        return memory

    raise AccessDeniedException()
