from app.exceptions.business_exception import BusinessException

class EmailAlreadyExistsException(BusinessException):
    status_code: int = 409
    detail: str = "Пользователь с таким e-mail уже зарегистрирован"
