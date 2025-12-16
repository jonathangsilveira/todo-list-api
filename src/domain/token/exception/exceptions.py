from src.core.exception.exceptions import UnauthorizedException


class TokenException(UnauthorizedException):
    pass


class InvalidTokenException(TokenException):
    pass


class ExpiredTokenException(TokenException):
    pass


class RevokedTokenException(TokenException):
    pass


class DecodeTokenException(TokenException):
    pass


class EncodeTokenException(TokenException):
    pass