from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: str
    full_name: str
    email: str
    password: str
    created_at: datetime
    last_update_at: Optional[datetime] = None
    is_active: bool = True

@dataclass
class UserCreation:
    email: str
    full_name: str
    password: str
    is_active: bool = True

@dataclass
class UserUpdate:
    id: str
    email: str
    full_name: str
    password: str
    is_active: bool