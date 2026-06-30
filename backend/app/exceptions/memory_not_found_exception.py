from app.exceptions.business_exception import BusinessException

class MemoryNotFoundException(BusinessException):
    status_code: int = 404
    detail: str = "Воспоминание не найдено"
