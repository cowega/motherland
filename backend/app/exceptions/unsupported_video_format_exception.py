from app.exceptions.business_exception import BusinessException

class UnsupportedVideoFormatException(BusinessException):
    status_code: int = 400
    detail: str = "Поддерживаются только видеоформаты MP4 и MOV."
