from src.domain.tasks.service.todo_tasks_service import TodoTasksService
from src.infra.tasks.adapter.in_memory_todo_tasks_repository import InMemoryTodoTasksRepository
from src.infra.user.repository.in_memory_user_repository import InMemoryUserRepository


def get_todo_tasks_service() -> TodoTasksService:
    repository = InMemoryTodoTasksRepository()
    return TodoTasksService(todo_tasks_repository=repository)