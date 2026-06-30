from app.exceptions.business_exception import BusinessException

class AccessDeniedException(BusinessException):
    status_code: int = 403
    detail: str = "Доступ ограничен"
