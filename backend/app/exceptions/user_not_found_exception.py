from app.exceptions.business_exception import BusinessException

class UserNotFoundException(BusinessException):
    status_code: int = 404
    detail: str = "Пользователь не найден"
