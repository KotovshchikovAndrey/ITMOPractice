from domain.exceptions.api_exception import ApiException, ApiExceptionStatus


class CoordinatesOccupied(ApiException):
    status = ApiExceptionStatus.BAD_REQUEST
    message = "Координаты уже заняты!"

    def __init__(self) -> None:
        super().__init__(status=self.status, message=self.message)
