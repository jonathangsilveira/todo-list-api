from pydantic import BaseModel

from src.domain.auth.model.auth_token import AuthToken


class AuthTokenResponse(BaseModel):
    refresh_token: str
    access_token: str
    expires_at: int
    token_type: str

    @staticmethod
    def from_domain(auth_token: AuthToken) -> "AuthTokenResponse":
        return AuthTokenResponse(
            refresh_token=auth_token.refresh_token,
            access_token=auth_token.access_token,
            expires_at=auth_token.expires_at,
            token_type=auth_token.type
        )