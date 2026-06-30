from app.schemas.user import UserBase, UserCreate, UserResponse, UserLogin, Token, TokenData
from app.schemas.location import PointSchema, LocationBase, LocationCreate, LocationResponse
from app.schemas.memory import MemoryBase, MemoryCreate, MemoryResponse
from app.schemas.media_file import MediaFileBase, MediaFileCreate, MediaFileResponse
from app.schemas.resident import ResidentBase, ResidentCreate, ResidentResponse
from app.schemas.photo_tag import PhotoTagBase, PhotoTagCreate, PhotoTagResponse

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenData",
    # Location
    "PointSchema",
    "LocationBase",
    "LocationCreate",
    "LocationResponse",
    # Memory
    "MemoryBase",
    "MemoryCreate",
    "MemoryResponse",
    # MediaFile
    "MediaFileBase",
    "MediaFileCreate",
    "MediaFileResponse",
    # Resident
    "ResidentBase",
    "ResidentCreate",
    "ResidentResponse",
    # PhotoTag
    "PhotoTagBase",
    "PhotoTagCreate",
    "PhotoTagResponse",
]
