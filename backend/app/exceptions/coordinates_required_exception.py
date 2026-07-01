from app.exceptions.business_exception import BusinessException

class CoordinatesRequiredException(BusinessException):
    status_code: int = 400
    detail: str = "Координаты обязательны для населенного пункта и здания"
