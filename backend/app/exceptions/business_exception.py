class BusinessException(Exception):
    status_code: int = 400
    detail: str = "Произошла ошибка бизнес-логики"

    def __init__(self, detail: str = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)
