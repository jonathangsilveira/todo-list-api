

class TokenException(Exception):
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