from dependency_injector import containers, providers
from dependency_injector.containers import WiringConfiguration

from src.domain.auth.service.auth_service import AuthService
from src.domain.password.service.password_service import PasswordService
from src.domain.tasks.service.todo_tasks_service import TodoTasksService
from src.domain.token.service.token_service import TokenService
from src.domain.user.service.user_service import UserService
from src.infra.password.bcrypt_password_hasher import BcryptPasswordHasher
from src.infra.tasks.adapter.in_memory_todo_tasks_repository import InMemoryTodoTasksRepository
from src.infra.user.repository.in_memory_user_repository import InMemoryUserRepository


class DependencyContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    wiring_config = WiringConfiguration(
        modules=[
            "src.domain.user.service.user_service",
            "src.infra.user.repository.in_memory_user_repository",
            "src.domain.tasks.service.todo_tasks_service",
            "src.infra.tasks.adapter.in_memory_todo_tasks_repository",
            "src.domain.auth.service.auth_service",
            "src.infra.password.bcrypt_password_hasher",
            "src.domain.token.service.token_service",
            "src.api.auth.dependencies"
        ]
    )

    user_service = providers.Factory(
        provides=UserService,
        user_repository=InMemoryUserRepository
    )

    todo_tasks_service = providers.Factory(
        provides=TodoTasksService,
        todo_tasks_repository=InMemoryTodoTasksRepository()
    )

    auth_service = providers.Factory(
        provides=AuthService,
        password_service=PasswordService(
            hasher=BcryptPasswordHasher(),
            salt_length=config.salt_length,
        ),
        token_service=TokenService(secret_key=config.secret_key),
        user_service=user_service
    )