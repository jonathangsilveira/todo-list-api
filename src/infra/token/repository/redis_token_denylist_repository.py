from redis.asyncio import Redis

from src.domain.token.repository.token_denylist_repository import TokenDenylistRepository


class RedisTokenDenylistRepository(TokenDenylistRepository):

    def __init__(self, redis_client: Redis):
        self._redis_client = redis_client

    async def token_exists(self, jti: str) -> bool:
        if await self._redis_client.get(jti):
            return True
        return False

    async def add_token(self, jti: str, ttl: int):
        await self._redis_client.setex(name=jti, time=ttl, value="revoked")