import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from src.domain.auth.exceptions.expired_access_token import ExpiredAccessTokenException
from src.domain.auth.exceptions.invalid_access_token import InvalidAccessTokenException
from src.domain.auth.service.auth_service import AuthService
from src.domain.password.service.password_service import PasswordService
from src.domain.token.service.token_service import TokenService
from src.domain.user.exception.user_not_found import UserNotFoundException
from src.domain.user.model.user import User
from src.domain.user.service.user_service import UserService
from src.infra.password.bcrypt_password_hasher import BcryptPasswordHasher
from src.infra.token.repository.in_memory_token_denylist_repository import InMemoryTokenDenylistRepository
from src.infra.user.repository.in_memory_user_repository import InMemoryUserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/v1/signin")


def get_auth_service() -> AuthService:
    password_service = get_password_service()
    token_service = get_token_service()
    user_service = get_user_service()
    return AuthService(
        password_service=password_service,
        token_service=token_service,
        user_service=user_service
    )


async def get_authorized_user(access_token: str = Depends(oauth2_scheme),
                              auth_service: AuthService = Depends(get_auth_service)) -> User:
    try:
        return await auth_service.get_current_user_by_access_token(access_token=access_token)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid username",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except (InvalidAccessTokenException, ExpiredAccessTokenException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_password_service() -> PasswordService:
    salt_length = int(os.getenv("GEN_SALT_ROUNDS", 9))
    return PasswordService(hasher=BcryptPasswordHasher(), salt_length=salt_length)


def get_token_service() -> TokenService:
    secret_key = os.getenv("AUTH_SECRET_KEY")
    return TokenService(secret_key=secret_key, denylist_repository=InMemoryTokenDenylistRepository())


def get_user_service() -> UserService:
    return UserService(user_repository=InMemoryUserRepository())