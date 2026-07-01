from app.exceptions.business_exception import BusinessException

class ParentLocationRequiredException(BusinessException):
    status_code: int = 400
    detail: str = "Для данного типа локации требуется указать родительский объект."
