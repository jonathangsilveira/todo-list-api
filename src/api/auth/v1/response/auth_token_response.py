from pydantic import BaseModel

from src.domain.auth.model.auth_token import AuthToken


class AuthTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    @staticmethod
    def from_domain(auth_token: AuthToken) -> "AuthTokenResponse":
        return AuthTokenResponse(
            access_token=auth_token.access_token,
            refresh_token=auth_token.refresh_token,
            token_type=auth_token.type
        )