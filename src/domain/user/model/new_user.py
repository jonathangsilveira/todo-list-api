from dataclasses import dataclass


@dataclass
class NewUser:
    full_name: str
    email: str
    password: str
    is_active: bool = True