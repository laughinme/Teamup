from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from domain.errors import ErrorBody, ErrorResponse


UNKNOWN_ERROR_CODE = "UNKNOWN_ERROR"
UNKNOWN_ERROR_MESSAGE = "Unknown error"
ERROR_CODES_BY_STATUS = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    409: "CONFLICT",
    412: "PRECONDITION_FAILED",
    500: "INTERNAL_SERVER_ERROR",
    501: "NOT_IMPLEMENTED",
    502: "BAD_GATEWAY",
}

def _build_payload(code: str, message: str) -> dict:
    payload = ErrorResponse(error=ErrorBody(code=code, message=message))
    return payload.model_dump()


def _resolve_code(status_code: int, explicit_code: str | None = None) -> str:
    if explicit_code:
        return explicit_code
    return ERROR_CODES_BY_STATUS.get(status_code, UNKNOWN_ERROR_CODE)


def setup_error_handlers(app: FastAPI):
    """Setup reusable error handlers for the app."""

    # @app.exception_handler(ApplicationHTTPError)
    # async def application_http_error_handler(request: Request, exc: ApplicationHTTPError):
    #     status_code = getattr(exc, "status_code", 500)
    #     message = getattr(exc, "message", UNKNOWN_ERROR_MESSAGE)
    #     error_code = _resolve_code(status_code, getattr(exc, "error_code", None))
    #     return JSONResponse(
    #         status_code=status_code,
    #         content=_build_payload(error_code, message),
    #     )

    @app.exception_handler(HTTPException)
    async def fastapi_http_exception_handler(request: Request, exc: HTTPException):
        if isinstance(exc.detail, str):
            message = exc.detail
        else:
            message = str(exc.detail) if exc.detail else UNKNOWN_ERROR_MESSAGE
        error_code = _resolve_code(exc.status_code)
        return JSONResponse(
            status_code=exc.status_code,
            content=_build_payload(error_code, message),
        )

    @app.exception_handler(Exception)
    async def fallback_exception_handler(request: Request, exc: Exception):
        message = UNKNOWN_ERROR_MESSAGE
        return JSONResponse(
            status_code=500,
            content=_build_payload(UNKNOWN_ERROR_CODE, message),
        )
