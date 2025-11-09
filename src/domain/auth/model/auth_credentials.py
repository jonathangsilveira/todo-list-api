from dataclasses import dataclass


@dataclass
class AuthCredentials:
    email: str
    password: str