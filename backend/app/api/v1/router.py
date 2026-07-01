from fastapi import APIRouter
from app.api.v1.endpoints import auth, locations, memories

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(locations.router, prefix="/locations", tags=["locations"])
api_router.include_router(memories.router, prefix="/memories", tags=["memories"])
