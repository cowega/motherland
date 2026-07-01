from app.exceptions.business_exception import BusinessException

class ImageResolutionExceededException(BusinessException):
    status_code: int = 400
    detail: str = "Разрешение изображения превышает лимит 4096x4096 пикселей."
