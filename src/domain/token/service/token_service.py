from logging import getLogger
from typing import Optional

import jwt
from jwt import ExpiredSignatureError

from src.domain.token.model.jwt_payload import JwtPayload
from src.domain.token.model.token import Token
from src.domain.token.model.token_status import TokenStatus

logger = getLogger(__name__)


class TokenService:

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self._secret_key = secret_key
        self._algorithm = algorithm

    def create_token(self, jwt_payload: JwtPayload) -> Token:
        payload = {"sub": jwt_payload.sub, "exp": jwt_payload.exp}
        jwt_token = jwt.encode(payload=payload, key=self._secret_key, algorithm=self._algorithm)
        return Token(value=jwt_token)

    def get_subject_from_token(self, jwt_token: str) -> Optional[str]:
        payload = jwt.decode(jwt=jwt_token, key=self._secret_key,
                             algorithms=[self._algorithm], verify=False)
        return payload.get("sub")

    def get_token_status(self, jwt_token: str):
        try:
            jwt.decode(jwt=jwt_token, key=self._secret_key,
                       algorithms=[self._algorithm], verify=False)
            return TokenStatus.VALID
        except ExpiredSignatureError as expired:
            logger.error(msg=f"Token has expired: {str(expired)}")
            return TokenStatus.EXPIRED
        except Exception as error:
            logger.error(msg=f"Error on decode access token: {str(error)}")
            return TokenStatus.INVALID
