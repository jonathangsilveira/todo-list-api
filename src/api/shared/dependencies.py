from fastapi.params import Depends
from starlette.requests import Request

from src.domain.user.repository.user_repository import UserRepository
from src.domain.user.service.user_service import UserService
from src.infra.database.sqlite.session.async_session_factory import AsyncSessionFactory
from src.infra.user.adapter.local_users_repository import LocalUsersRepository


def get_async_session_factory(request: Request) -> AsyncSessionFactory:
    return request.app.state.async_session_factory


async def get_user_repository(
        async_session_factory: AsyncSessionFactory = Depends(get_async_session_factory)) -> UserRepository:
    return LocalUsersRepository(async_session_factory)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=user_repository)
