from app.exceptions.business_exception import BusinessException

class InvalidRoomParentException(BusinessException):
    status_code: int = 400
    detail: str = "Родителем комнаты/квартиры может быть только здание."
