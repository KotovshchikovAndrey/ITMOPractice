from domain.exceptions.api_exception import ApiException, ApiExceptionStatus


class PointAlreadyInFavorite(ApiException):
    status = ApiExceptionStatus.BAD_REQUEST
    message = "Городская точка уже в избранном!"

    def __init__(self) -> None:
        super().__init__(status=self.status, message=self.message)
