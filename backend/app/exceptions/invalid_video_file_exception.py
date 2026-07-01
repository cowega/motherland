from app.exceptions.business_exception import BusinessException

class InvalidVideoFileException(BusinessException):
    status_code: int = 400
    detail: str = "Некорректный или поврежденный файл видео."
