from src.core.exception.exceptions import UnauthorizedException, InternalErrorException


class TokenException(InternalErrorException):
    pass


class InvalidTokenException(UnauthorizedException):
    pass


class ExpiredTokenException(UnauthorizedException):
    pass


class RevokedTokenException(UnauthorizedException):
    pass


class DecodeTokenException(TokenException):
    pass


class EncodeTokenException(TokenException):
    pass