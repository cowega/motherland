from app.exceptions.business_exception import BusinessException

class VideoSizeExceededException(BusinessException):
    status_code: int = 400
    detail: str = "Размер видео превышает лимит 100 МБ"
