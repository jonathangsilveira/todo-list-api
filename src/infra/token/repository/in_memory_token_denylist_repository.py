from src.domain.token.repository.token_denylist_repository import TokenDenylistRepository


class InMemoryTokenDenylistRepository(TokenDenylistRepository):
    _denylist_store = {}

    async def token_exists(self, jti: str) -> bool:
        ttl = self._denylist_store.get(jti)
        if not ttl:
            return False

        return True

    async def add_token(self, jti: str, ttl: int):
        self._denylist_store[jti] = ttl