from unittest.mock import patch, AsyncMock

import pytest

from src.domain.token.exception.exceptions import EncodeTokenException, DecodeTokenException, RevokedTokenException, \
    ExpiredTokenException
from src.domain.token.model.jwt_payload import JwtPayload
from src.domain.token.service.token_service import TokenService


class TestTokenService:

    @pytest.mark.asyncio
    async def test_create_token_success(self, jwt_payload_stub: JwtPayload, token_service: TokenService):
        _ = token_service.create_token(jwt_payload=jwt_payload_stub)

    @pytest.mark.asyncio
    @patch(target="jwt.encode", side_effect=ValueError("error"))
    async def test_create_token_encode_token_exception(self, jwt_payload_stub: JwtPayload, token_service: TokenService):
        with pytest.raises(EncodeTokenException):
            _ = token_service.create_token(jwt_payload=jwt_payload_stub)

    @pytest.mark.asyncio
    async def test_decode_token_success(self, jwt_payload_stub: JwtPayload, token_service: TokenService):
        # Given
        jwt_token = token_service.create_token(jwt_payload=jwt_payload_stub)

        # When
        jwt_payload = await token_service.decode_token(jwt_token=jwt_token.value)

        # Then
        assert jwt_payload.sub == jwt_payload_stub.sub
        assert jwt_payload.jti == jwt_payload_stub.jti

    @pytest.mark.asyncio
    @patch(target="jwt.decode", side_effect=ValueError("error"))
    async def test_decode_token_decode_token_exception(self, jwt_payload_stub: JwtPayload, token_service: TokenService):
        with pytest.raises(DecodeTokenException):
            _ = await token_service.decode_token(jwt_token="token")

    @pytest.mark.asyncio
    async def test_decode_token_revoked_token_exception(self, jwt_payload_stub: JwtPayload,
                                                        token_denylist_repository_mock, token_service: TokenService):
        # Given
        token_denylist_repository_mock.token_exists = AsyncMock(return_value=True)
        token = token_service.create_token(jwt_payload_stub)

        # When
        with pytest.raises(RevokedTokenException):
            _ = await token_service.decode_token(jwt_token=token.value)

    @pytest.mark.asyncio
    async def test_decode_token_expired_token_exception(self, expired_jwt_payload_stub: JwtPayload,
                                                        token_service: TokenService):
        # Given
        token = token_service.create_token(expired_jwt_payload_stub)

        # When
        with pytest.raises(ExpiredTokenException):
            _ = await token_service.decode_token(jwt_token=token.value)