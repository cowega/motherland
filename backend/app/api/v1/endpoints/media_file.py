import os
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.memory import Memory
from app.models.media_file import MediaFile, MediaType
from app.models.user import User
from app.schemas.media_file import MediaFileResponse
from app.api.deps import get_current_user
from app.services.s3 import upload_file_async
from app.services.media import process_image, get_mp4_duration
from app.exceptions import (
    MemoryNotFoundException,
    AccessDeniedException,
    VideoSizeExceededException,
    VideoDurationExceededException,
    ImageSizeExceededException,
    InvalidImageFileException,
    InvalidVideoFileException,
    UnsupportedVideoFormatException,
    UnsupportedFileFormatException
)

router = APIRouter()


@router.post("/{memory_id}/media", response_model=MediaFileResponse, status_code=status.HTTP_201_CREATED)
async def upload_media(
    memory_id: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> MediaFile:
    memory_query = select(Memory).where(Memory.id == memory_id)
    memory_result = await db.execute(memory_query)
    memory = memory_result.scalars().first()
    if not memory:
        raise MemoryNotFoundException()

    if memory.user_id != current_user.id:
        raise AccessDeniedException()

    content_type = file.content_type or ""
    filename = os.path.basename(file.filename or "file")

    is_image = content_type.startswith("image/") or filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif"))
    is_video = content_type.startswith("video/") or filename.lower().endswith((".mp4", ".mov", ".avi", ".webm"))

    if not is_image and not is_video:
        raise UnsupportedFileFormatException()

    if is_image:
        limit = 15 * 1024 * 1024
    else:
        limit = 100 * 1024 * 1024

    if file.size and file.size > limit:
        if is_image:
            raise ImageSizeExceededException()
        else:
            raise VideoSizeExceededException()

    # Безопасное чтение файла чанками для защиты от DoS по памяти
    file_bytes = b""
    chunk_size = 1024 * 1024  # 1 MB
    try:
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            file_bytes += chunk
            if len(file_bytes) > limit:
                if is_image:
                    raise ImageSizeExceededException()
                else:
                    raise VideoSizeExceededException()
    finally:
        await file.close()

    size_bytes = len(file_bytes)

    if is_image:
        media_type = MediaType.photo
        try:
            processed_bytes = process_image(file_bytes)
        except Exception:
            raise InvalidImageFileException()
        size_bytes = len(processed_bytes)
        s3_filename = f"memories/{memory_id}/{uuid4()}.webp"
        file_url = await upload_file_async(processed_bytes, s3_filename, "image/webp")
        duration_seconds = None
        original_date = None
    else:
        ext = filename.lower()
        if ext.endswith(".mp4"):
            safe_ext = ".mp4"
            safe_content_type = "video/mp4"
        elif ext.endswith(".mov"):
            safe_ext = ".mov"
            safe_content_type = "video/quicktime"
        else:
            raise UnsupportedVideoFormatException()

        media_type = MediaType.video

        duration = get_mp4_duration(file_bytes)
        if duration <= 0:
            raise InvalidVideoFileException()
        if duration > 60.0:
            raise VideoDurationExceededException()

        s3_filename = f"memories/{memory_id}/{uuid4()}{safe_ext}"
        file_url = await upload_file_async(file_bytes, s3_filename, safe_content_type)
        duration_seconds = int(duration)
        original_date = None

    db_media = MediaFile(
        memory_id=memory_id,
        uploaded_by=current_user.id,
        file_url=file_url,
        file_type=media_type,
        size_bytes=size_bytes,
        duration_seconds=duration_seconds,
        original_date=original_date
    )

    db.add(db_media)
    await db.commit()
    await db.refresh(db_media)
    return db_media
