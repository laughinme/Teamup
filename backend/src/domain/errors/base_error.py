from pydantic import BaseModel


# class ApplicationHTTPError(Exception):
#     """Base application HTTP error exposing HTTP metadata."""

#     status_code = 500
#     error_code = "UNKNOWN_ERROR"
#     default_message = "Unknown error"

#     def __init__(self, message: str | None = None):
#         self.message = message or self.default_message

#     def __str__(self) -> str:
#         return self.message


class ErrorBody(BaseModel):
    code: str
    message: str

class ErrorResponse(BaseModel):
    error: ErrorBody
