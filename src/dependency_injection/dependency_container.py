from dependency_injector import containers, providers
from dependency_injector.containers import WiringConfiguration

from src.domain.auth.service.auth_service import AuthService
from src.domain.password.service.password_service import PasswordService
from src.domain.tasks.service.todo_tasks_service import TodoTasksService
from src.domain.token.service.token_service import TokenService
from src.domain.user.service.user_service import UserService
from src.infra.database.redis.client import create_redis_client
from src.infra.password.bcrypt_password_hasher import BcryptPasswordHasher
from src.infra.tasks.adapter.in_memory_todo_tasks_repository import InMemoryTodoTasksRepository
from src.infra.token.repository.redis_token_denylist_repository import RedisTokenDenylistRepository
from src.infra.user.repository.in_memory_user_repository import InMemoryUserRepository
from src.settings.app_settings import AppSettings


class DependencyContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    wiring_config = WiringConfiguration(
        modules=[
            "src.infra.database.redis.client",
            "src.domain.user.service.user_service",
            "src.infra.user.repository.in_memory_user_repository",
            "src.domain.tasks.service.todo_tasks_service",
            "src.infra.tasks.adapter.in_memory_todo_tasks_repository",
            "src.domain.auth.service.auth_service",
            "src.infra.password.bcrypt_password_hasher",
            "src.domain.token.service.token_service",
            "src.settings.app_settings",
            "src.api.auth.dependencies"
        ]
    )

    app_settings = providers.Singleton(provides=AppSettings)

    redis_client = providers.Singleton(
        provides=create_redis_client
    )

    user_service = providers.Factory(
        provides=UserService,
        user_repository=InMemoryUserRepository()
    )

    todo_tasks_service = providers.Factory(
        provides=TodoTasksService,
        todo_tasks_repository=InMemoryTodoTasksRepository()
    )

    token_denylist_repository = providers.Factory(
        provides=RedisTokenDenylistRepository,
        redis_client=redis_client
    )

    token_service = providers.Factory(
        provides=TokenService,
        denylist_repository=token_denylist_repository,
        secret_key=app_settings().auth_secret_key,
        algorithm="HS256"
    )

    password_service = providers.Factory(
        provides=PasswordService,
        hasher=BcryptPasswordHasher(),
        salt_length=app_settings().gen_salt_rounds,
        encoding="utf-8"
    )

    auth_service = providers.Factory(
        provides=AuthService,
        password_service=password_service,
        token_service=token_service,
        user_service=user_service
    )