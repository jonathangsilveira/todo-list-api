from enum import StrEnum


class TokenStatus(StrEnum):
    VALID = "valid"
    INVALID = "invalid"
    EXPIRED = "expired"