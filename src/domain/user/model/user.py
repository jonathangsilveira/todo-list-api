from dataclasses import dataclass


@dataclass
class User:
    uuid: str
    full_name: str
    email: str
    password: str
    is_active: bool = True