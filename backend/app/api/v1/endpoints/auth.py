from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.exceptions import EmailAlreadyExistsException, InvalidCredentialsException

router = APIRouter()

@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_db)) -> Token:
    """
    Register a new user and return a JWT access token.
    """
    # Check if user already exists
    query = select(User).where(User.email == user_in.email)
    result = await db.execute(query)
    existing_user = result.scalars().first()
    if existing_user:
        raise EmailAlreadyExistsException()
    
    # Create new user
    db_user = User(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        full_name=user_in.full_name
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    # Create token
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return Token(access_token=access_token, token_type="bearer")

@router.post("/login", response_model=Token)
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)) -> Token:
    """
    Log in user and return a JWT access token.
    """
    # Find user by email
    query = select(User).where(User.email == user_in.email)
    result = await db.execute(query)
    db_user = result.scalars().first()
    if not db_user:
        raise InvalidCredentialsException()
    
    # Verify password
    if not verify_password(user_in.password, db_user.password_hash):
        raise InvalidCredentialsException()
    
    # Create token
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return Token(access_token=access_token, token_type="bearer")
