from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.core.exception.exceptions import InternalErrorException, BusinessException, NotFoundException, AppException, \
    ConflictException, UnauthorizedException


def setup_exception_handling(app: FastAPI):
    @app.exception_handler(exc_class_or_status_code=InternalErrorException)
    def internal_error_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": exc.message},
        )

    @app.exception_handler(exc_class_or_status_code=BusinessException)
    def bad_request_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": exc.message},
        )

    @app.exception_handler(exc_class_or_status_code=NotFoundException)
    def not_found_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": exc.message},
        )

    @app.exception_handler(exc_class_or_status_code=ConflictException)
    def conflict_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": exc.message},
        )

    @app.exception_handler(exc_class_or_status_code=UnauthorizedException)
    def unauthorized_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            content={"message": exc.message},
        )