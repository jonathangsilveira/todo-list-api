from datetime import timedelta
from logging import getLogger

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from src.core.exception.exceptions import InternalErrorException
from src.domain.token.exception.exceptions import ExpiredTokenException, InvalidTokenException, TokenException, \
    RevokedTokenException, EncodeTokenException, DecodeTokenException
from src.domain.token.model.jwt_payload import JwtPayload
from src.domain.token.model.token import Token
from src.domain.token.model.token_status import TokenStatus
from src.domain.token.repository.token_denylist_repository import TokenDenylistRepository

logger = getLogger(__name__)


class TokenService:

    def __init__(self, denylist_repository: TokenDenylistRepository, secret_key: str, algorithm: str = "HS256"):
        self._denylist_repository = denylist_repository
        self._secret_key = secret_key
        self._algorithm = algorithm

    def create_token(self, jwt_payload: JwtPayload) -> Token:
        try:
            payload = {
                "sub": jwt_payload.sub,
                "exp": jwt_payload.exp,
                "iat": jwt_payload.iat,
                "jti": jwt_payload.jti
            }
            jwt_token = jwt.encode(payload=payload, key=self._secret_key, algorithm=self._algorithm)
            return Token(value=jwt_token, expires_at=jwt_payload.exp)
        except Exception as error:
            logger.error(msg="Error on encode token", exc_info=error)
            raise EncodeTokenException(message="Error on encode token")

    async def revoke_token(self, jwt_token: str):
        payload = await self.decode_token(jwt_token)
        diff = payload.exp - payload.iat
        await self._denylist_repository.add_token(jti=payload.jti, ttl=diff)

    async def decode_token(self, jwt_token: str) -> JwtPayload:
        try:
            payload = jwt.decode(jwt=jwt_token, key=self._secret_key,
                                 algorithms=[self._algorithm], verify=False)

            jwt_payload = JwtPayload(**payload)

            is_token_denied = await self._denylist_repository.token_exists(jwt_payload.jti)
            if is_token_denied:
                raise RevokedTokenException(message="Token has been revoked")

            return jwt_payload
        except ExpiredSignatureError as expired:
            logger.error(msg="Token has expired", exc_info=expired)
            raise ExpiredTokenException(message="Token has expired")
        except InvalidTokenError as invalid:
            logger.error(msg="Invalid token", exc_info=invalid)
            raise InvalidTokenException(message="Invalid token")
        except RevokedTokenException:
            logger.error(msg="Token has been revoked")
            raise
        except InternalErrorException as exc:
            logger.error(msg="Internal error", exc_info=exc)
            raise exc
        except Exception as error:
            logger.error(msg="Error on decode token", exc_info=error)
            raise DecodeTokenException(message="Error on decode token")

    async def get_token_status(self, jwt_token: str):
        try:
            _ = await self.decode_token(jwt_token)
            return TokenStatus.VALID
        except ExpiredTokenException:
            return TokenStatus.EXPIRED
        except RevokedTokenException:
            return TokenStatus.REVOKED
        except TokenException:
            return TokenStatus.INVALID
