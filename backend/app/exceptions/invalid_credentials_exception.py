from app.exceptions.business_exception import BusinessException

class InvalidCredentialsException(BusinessException):
    status_code: int = 401
    detail: str = "Неверный e-mail или пароль"
