from fastapi import HTTPException


class BadRequestHTTPError(HTTPException):
    def __init__(self, detail: str | None = None):
        super().__init__(status_code=400, detail=detail or "Bad request")
