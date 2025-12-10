from datetime import datetime
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


@pytest_asyncio.fixture(scope="package")
def token_service(token_denylist_repository_mock: TokenDenylistRepository) -> TokenService:
    return TokenService(denylist_repository=token_denylist_repository_mock, secret_key="chablau")


@pytest.fixture(scope="package")
def jwt_payload_stub() -> JwtPayload:
    return JwtPayload(
        sub="chablau@chablau.com",
        iat=datetime.fromtimestamp(1765123065),
        exp=datetime.fromtimestamp(1765209465),
        jti="04302e0b-3ba1-4c28-ab3e-2b1de6a4d22b"
    )

@pytest.fixture(scope="package")
def jwt_token_stub() -> str:
    header = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
    payload = 'eyJzdWIiOiJjaGFibGF1QGNoYWJsYXUuY29tIiwiZXhwIjoxNzY1MjA5NDY1LCJpYXQiOjE3NjUxMjMwNjUsImp0aSI6IjA0MzAyZTBiLTNiYTEtNGMyOC1hYjNlLTJiMWRlNmE0ZDIyYiJ9'
    signature = 'qDJhWobkrCZNuGOAiIduJ7ajzGMc4K6pt0AKkvOaZmM'
    return f"{header}.{payload}.{signature}"