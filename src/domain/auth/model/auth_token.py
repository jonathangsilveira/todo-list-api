from dataclasses import dataclass


@dataclass
class AuthToken:
    access_token: str
    refresh_token: str
    type: str = "Bearer"