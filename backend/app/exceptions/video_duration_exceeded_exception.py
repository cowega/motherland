from app.exceptions.business_exception import BusinessException

class VideoDurationExceededException(BusinessException):
    status_code: int = 400
    detail: str = "Длительность видео превышает лимит 60 секунд"
