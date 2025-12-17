from typing import Optional


class AppException(Exception):
    message: str

    def __init__(self, message: Optional[str] = None):
        self.message = message or "An error occurred in application"
        super().__init__(self.message)


class BusinessException(AppException):
    pass


class NotFoundException(AppException):
    pass


class ConflictException(AppException):
    pass


class InternalErrorException(AppException):
    pass


class UnauthorizedException(AppException):
    pass