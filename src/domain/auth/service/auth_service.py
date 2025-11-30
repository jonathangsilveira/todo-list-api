from datetime import datetime, timezone, timedelta

from src.domain.auth.exceptions.expired_access_token import ExpiredAccessTokenException
from src.domain.auth.exceptions.invalid_access_token import InvalidAccessTokenException
from src.domain.auth.model.auth_credentials import AuthCredentials
from src.domain.auth.model.auth_token import AuthToken
from src.domain.password.exception.invalid_password import InvalidPasswordException
from src.domain.password.service.password_service import PasswordService
from src.domain.token.model.jwt_payload import JwtPayload
from src.domain.token.model.token import Token
from src.domain.token.model.token_status import TokenStatus
from src.domain.token.service.token_service import TokenService
from src.domain.user.exception.user_not_found import UserNotFoundException
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
        if not user:
            raise UserNotFoundException()
        is_valid_password = self._password_service.is_valid_password(auth_credentials.password, user.password)
        if not is_valid_password:
            raise InvalidPasswordException()
        access_token = await self._create_access_token(user)
        refresh_token = await self._create_refresh_token(user)
        return AuthToken(
            access_token=access_token.value,
            refresh_token=refresh_token.value
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
        self._check_token_status(access_token)
        email = self._token_service.get_subject_from_token(jwt_token=access_token)
        user = await self._user_service.get_user_by_email(email)
        if not user:
            raise UserNotFoundException()
        return user

    def _check_token_status(self, access_token: str):
        access_token_status = self._token_service.get_token_status(access_token)
        if access_token_status == TokenStatus.EXPIRED:
            raise ExpiredAccessTokenException()
        elif access_token_status == TokenStatus.INVALID:
            raise InvalidAccessTokenException()

    async def _create_refresh_token(self, user: User) -> Token:
        refresh_expiration_datetime = datetime.now(timezone.utc) + timedelta(days=7)
        refresh_jwt_payload = JwtPayload(sub=user.email, exp=refresh_expiration_datetime)
        refresh_token = self._token_service.create_token(refresh_jwt_payload)
        return refresh_token

    async def _create_access_token(self, user: User) -> Token:
        access_expiration_datetime = datetime.now(timezone.utc) + timedelta(days=1)
        access_jwt_payload = JwtPayload(sub=user.email, exp=access_expiration_datetime)
        access_token = self._token_service.create_token(access_jwt_payload)
        return access_token