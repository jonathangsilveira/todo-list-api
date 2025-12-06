from dataclasses import dataclass


@dataclass
class Token:
    value: str
    type: str = "Bearer"