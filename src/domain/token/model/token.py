from dataclasses import dataclass


@dataclass(eq=True, frozen=True, slots=True)
class Token:
    value: str
    type: str = "Bearer"