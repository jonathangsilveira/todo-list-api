from dataclasses import dataclass
from datetime import datetime


@dataclass(eq=True, frozen=True, slots=True)
class Token:
    value: str
    expires_at: datetime
    type: str = "Bearer"