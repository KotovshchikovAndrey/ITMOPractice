import typing as tp
from enum import StrEnum


class ApiExceptionStatus(StrEnum):
    NOT_FOUND = "not found"
    FORBIDDEN = "forbidden"
    AUTHORIZED = "authorized"
    BAD_REQUEST = "bad request"
    INTERNAL = "internal"


class ApiException(Exception):
    status: ApiExceptionStatus
    message: str

    def __init__(self, status: ApiExceptionStatus, message: str) -> None:
        self.status = status
        self.message = message
