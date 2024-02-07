from domain.exceptions.api_exception import ApiException, ApiExceptionStatus


class InvalidTags(ApiException):
    status = ApiExceptionStatus.BAD_REQUEST
    message = "Недопустимые теги!"

    def __init__(self) -> None:
        super().__init__(status=self.status, message=self.message)
