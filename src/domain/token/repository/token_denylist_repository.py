from abc import ABC, abstractmethod
from datetime import timedelta


class TokenDenylistRepository(ABC):

    @abstractmethod
    async def token_exists(self, jti: str) -> bool:
        ...

    @abstractmethod
    async def add_token(self, jti: str, ttl: int):
        ...