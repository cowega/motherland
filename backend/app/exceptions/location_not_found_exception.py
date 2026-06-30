from app.exceptions.business_exception import BusinessException

class LocationNotFoundException(BusinessException):
    status_code: int = 404
    detail: str = "Локация не найдена"
