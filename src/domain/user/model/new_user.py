from dataclasses import dataclass


@dataclass
class NewUser:
    id: str
    full_name: str
    email: str
    password: str
    is_active: bool = True