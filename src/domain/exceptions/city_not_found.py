from domain.exceptions.api_exception import ApiException, ApiExceptionStatus


class CityNotFound(ApiException):
    status = ApiExceptionStatus.NOT_FOUND
    message = "Город не найден!"

    def __init__(self) -> None:
        super().__init__(status=self.status, message=self.message)
