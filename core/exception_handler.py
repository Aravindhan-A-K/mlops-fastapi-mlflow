from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.requests import Request
from core.logger import logger
from fastapi import status, FastAPI


def register_exception(app: FastAPI):

    @app.exception_handler(RequestValidationError)
    async def validate_request(request: Request, exc:RequestValidationError):
        logger.error("Request validation Failed!",
            extra ={
                "correlation_id": getattr(request.state, "correlation_id", None),
                "errors": exc.errors()
            })
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content = {
                "status": "error",
                "message": "Request validation failed",
                "details": exc.errors(),
                "correlation_id": getattr(request.state, "correlation_id", None)
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception(request: Request, exc: HTTPException):
        logger.error("Http exception occured",
                     extra={
                         "correlation_id": getattr(request.state, "correlation_id", None),
                         "errors": exc.detail,
                     })
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "message": "Http exception occured",
                "details": exc.detail,
                "correlation_id": getattr(request.state, "correlation_id", None)
                                
            }
        )
