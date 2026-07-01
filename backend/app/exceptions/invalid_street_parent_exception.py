from app.exceptions.business_exception import BusinessException

class InvalidStreetParentException(BusinessException):
    status_code: int = 400
    detail: str = "Родителем улицы может быть только населенный пункт."
