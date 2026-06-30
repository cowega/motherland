from typing import AsyncGenerator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.user import User
from app.core.security import decode_access_token
from app.exceptions import AccessDeniedException, UserNotFoundException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user.
    """
    payload = decode_access_token(token)
    if not payload:
        raise AccessDeniedException()
    
    user_id = payload.get("sub")
    if not user_id:
        raise AccessDeniedException()
    
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user:
        raise UserNotFoundException()
        
    return user
