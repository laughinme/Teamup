# from .base_error import ApplicationHTTPError
from fastapi import HTTPException


class NotImplementedHTTPError(HTTPException):
    def __init__(self, detail: str | None = None):
        super().__init__(status_code=501, detail=detail or "Not implemented")
