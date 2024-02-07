from domain.exceptions.api_exception import ApiException, ApiExceptionStatus


class EmailOccupied(ApiException):
    status = ApiExceptionStatus.BAD_REQUEST
    message = "Данный email занят!"

    def __init__(self) -> None:
        super().__init__(status=self.status, message=self.message)
