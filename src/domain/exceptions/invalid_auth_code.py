from domain.exceptions.api_exception import ApiException, ApiExceptionStatus


class InvalidAuthCode(ApiException):
    status = ApiExceptionStatus.FORBIDDEN
    message = "Неверный код!"

    def __init__(self) -> None:
        super().__init__(status=self.status, message=self.message)
