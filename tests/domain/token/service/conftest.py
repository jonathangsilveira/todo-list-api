from datetime import datetime, timedelta
from unittest.mock import MagicMock, AsyncMock

import pytest
import pytest_asyncio

from src.domain.token.model.jwt_payload import JwtPayload
from src.domain.token.repository.token_denylist_repository import TokenDenylistRepository
from src.domain.token.service.token_service import TokenService


@pytest_asyncio.fixture(scope="package")
def token_denylist_repository_mock() -> TokenDenylistRepository:
    repo = MagicMock(spec=TokenDenylistRepository)
    repo.add_token = AsyncMock()
    repo.token_exists = AsyncMock(return_value=False)
    return repo


@pytest_asyncio.fixture(scope="class")
def token_service(token_denylist_repository_mock: TokenDenylistRepository) -> TokenService:
    return TokenService(denylist_repository=token_denylist_repository_mock, secret_key="chablau")


@pytest.fixture(scope="function")
def jwt_payload_stub() -> JwtPayload:
    issued_at = datetime.now()
    return JwtPayload(
        sub="chablau@chablau.com",
        iat=issued_at,
        exp=issued_at + timedelta(days=1),
        jti="04302e0b-3ba1-4c28-ab3e-2b1de6a4d22b"
    )


@pytest.fixture(scope="function")
def expired_jwt_payload_stub() -> JwtPayload:
    issued_at = datetime.now()
    return JwtPayload(
        sub="chablau@chablau.com",
        iat=issued_at,
        exp=issued_at - timedelta(seconds=15),
        jti="jti-123"
    )