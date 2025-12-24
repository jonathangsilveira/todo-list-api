from redis.asyncio import Redis

from src.core.exception.exceptions import InternalErrorException
from src.domain.token.repository.token_denylist_repository import TokenDenylistRepository


class RedisTokenDenylistRepository(TokenDenylistRepository):

    def __init__(self, redis_client: Redis):
        self._redis_client = redis_client

    async def token_exists(self, jti: str) -> bool:
        try:
            key = self._generate_redis_key(jti)
            if await self._redis_client.get(key):
                return True
            return False
        except Exception as exc:
            raise InternalErrorException(message="Error fetching token JTI") from exc

    async def add_token(self, jti: str, ttl: int):
        try:
            await self._redis_client.setex(name=self._generate_redis_key(jti), time=ttl, value="revoked")
        except Exception as exc:
            raise InternalErrorException(message="Error adding token to denylist") from exc

    @staticmethod
    def _generate_redis_key(value: str) -> str:
        return f"token-denylist-{value}"