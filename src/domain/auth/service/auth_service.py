from datetime import datetime, timezone, timedelta

from src.domain.auth.model.auth_credentials import AuthCredentials
from src.domain.auth.model.auth_token import AuthToken
from src.domain.password.exception.invalid_password import InvalidPasswordException
from src.domain.password.service.password_service import PasswordService
from src.domain.token.model.jwt_payload import JwtPayload
from src.domain.token.model.token import Token
from src.domain.token.service.token_service import TokenService
from src.domain.user.model.user_models import User, UserCreation
from src.domain.user.service.user_service import UserService


class AuthService:

    def __init__(self, password_service: PasswordService, token_service: TokenService,
                 user_service: UserService):
        self._password_service = password_service
        self._token_service = token_service
        self._user_service = user_service

    async def authorize_login(self, auth_credentials: AuthCredentials) -> AuthToken:
        user = await self._user_service.get_user_by_email(auth_credentials.email)

        is_valid_password = self._password_service.is_valid_password(auth_credentials.password, user.password)
        if not is_valid_password:
            raise InvalidPasswordException()

        access_token = await self._create_token(subject=user.email, ttl=timedelta(days=1))
        refresh_token = await self._create_token(subject=user.email, ttl=timedelta(days=7))
        expires_at_millis = int(access_token.expires_at.timestamp() * 1000)
        return AuthToken(
            refresh_token=refresh_token.value,
            access_token=access_token.value,
            expires_at=expires_at_millis
        )

    async def register_new_user(self, full_name: str, email: str, password: str):
        hashed_password = self._password_service.generate_hash(password)
        new_user = UserCreation(
            full_name=full_name,
            email=email,
            password=hashed_password,
            is_active=True
        )
        await self._user_service.new_user(new_user)

    async def get_current_user_by_access_token(self, access_token: str) -> User:
        jwt_payload = await self._token_service.decode_token(access_token)
        return await self._user_service.get_user_by_email(jwt_payload.sub)

    async def signout(self, access_token: str):
        await self._token_service.revoke_token(access_token)

    async def refresh_token(self, refresh_token: str) -> AuthToken:
        jwt_payload = await self._token_service.decode_token(refresh_token)

        access_token = await self._create_token(subject=jwt_payload.sub, ttl=timedelta(days=1))
        expires_at_millis = int(access_token.expires_at.timestamp() * 1000)

        return AuthToken(
            refresh_token=refresh_token,
            access_token=access_token.value,
            expires_at=expires_at_millis
        )

    async def _create_token(self, subject: str, ttl: timedelta) -> Token:
        issued_at = datetime.now(timezone.utc)
        expires_at = issued_at + ttl
        jwt_payload = JwtPayload(
            sub=subject,
            iat=issued_at,
            exp=expires_at
        )
        return self._token_service.create_token(jwt_payload)
