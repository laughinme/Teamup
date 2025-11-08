from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from domain.errors import (
    ErrorBody,
    ErrorResponse,
    NotImplementedHTTPError,
)

def setup_error_handlers(app: FastAPI):
    """Setup error handlers for the app."""
    
    @app.exception_handler(NotImplementedHTTPError)
    async def not_implemented_handler(request: Request, exc: NotImplementedHTTPError):
        payload = ErrorResponse(error=ErrorBody(code="NOT_IMPLEMENTED", message=exc.message))
        return JSONResponse(status_code=501, content=payload.model_dump())

