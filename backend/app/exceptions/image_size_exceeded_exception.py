from app.exceptions.business_exception import BusinessException

class ImageSizeExceededException(BusinessException):
    status_code: int = 400
    detail: str = "Размер изображения превышает лимит 15 МБ"
