from domain.exceptions.api_exception import ApiException, ApiExceptionStatus


class UserNotFound(ApiException):
    status = ApiExceptionStatus.NOT_FOUND
    message = "пользователь не найден!"

    def __init__(self) -> None:
        super().__init__(status=self.status, message=self.message)
