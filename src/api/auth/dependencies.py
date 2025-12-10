from dependency_injector.wiring import inject, Provide
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from src.dependency_injection.dependency_container import DependencyContainer
from src.domain.auth.service.auth_service import AuthService
from src.domain.token.exception.exceptions import ExpiredTokenException, InvalidTokenException, RevokedTokenException, \
    TokenException
from src.domain.user.exception.user_not_found import UserNotFoundException
from src.domain.user.model.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/v1/signin")


@inject
def get_auth_service(auth_service: AuthService = Depends(Provide[DependencyContainer.auth_service])) -> AuthService:
    return auth_service


async def get_authorized_user(access_token: str = Depends(oauth2_scheme),
                              auth_service: AuthService = Depends(get_auth_service)) -> User:
    try:
        return await auth_service.get_current_user_by_access_token(access_token=access_token)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except RevokedTokenException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ExpiredTokenException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except TokenException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error encoding/decoding access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
