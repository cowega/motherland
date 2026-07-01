from app.exceptions.business_exception import BusinessException

class InvalidSettlementParentException(BusinessException):
    status_code: int = 400
    detail: str = "Родителем населенного пункта может быть только другой населенный пункт."
