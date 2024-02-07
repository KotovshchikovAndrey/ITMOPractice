from domain.exceptions.api_exception import ApiException, ApiExceptionStatus


class HttpExceptionStatusMapper:
    _exception: ApiException

    def __init__(self, exception: ApiException) -> None:
        self._exception = exception

    def do_mapping(self) -> int:
        match (self._exception.status):
            case ApiExceptionStatus.BAD_REQUEST:
                return 400

            case ApiExceptionStatus.AUTHORIZED:
                return 401

            case ApiExceptionStatus.FORBIDDEN:
                return 403

            case ApiExceptionStatus.NOT_FOUND:
                return 404

            case _:
                return 500
