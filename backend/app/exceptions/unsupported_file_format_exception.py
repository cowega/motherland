from app.exceptions.business_exception import BusinessException

class UnsupportedFileFormatException(BusinessException):
    status_code: int = 400
    detail: str = "Неподдерживаемый формат файла. Разрешены только фото и видео."
