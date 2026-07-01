from app.exceptions.business_exception import BusinessException

class InvalidBuildingParentException(BusinessException):
    status_code: int = 400
    detail: str = "Родителем здания может быть только улица."
