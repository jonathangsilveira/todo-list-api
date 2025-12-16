from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

from src.dependency_injection.dependency_container import DependencyContainer
from src.domain.auth.service.auth_service import AuthService
from src.domain.user.model.user_models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/v1/signin")


@inject
def get_auth_service(auth_service: AuthService = Depends(Provide[DependencyContainer.auth_service])) -> AuthService:
    return auth_service


async def get_authorized_user(access_token: str = Depends(oauth2_scheme),
                              auth_service: AuthService = Depends(get_auth_service)) -> User:
    return await auth_service.get_current_user_by_access_token(access_token=access_token)