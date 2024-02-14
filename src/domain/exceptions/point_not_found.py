from domain.exceptions.api_exception import ApiException, ApiExceptionStatus


class PointNotFound(ApiException):
    status = ApiExceptionStatus.NOT_FOUND
    message = "Точка не найдена!"

    def __init__(self) -> None:
        super().__init__(status=self.status, message=self.message)
