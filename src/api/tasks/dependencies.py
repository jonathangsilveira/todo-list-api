from src.domain.tasks.service.todo_tasks_service import TodoTasksService
from src.infra.tasks.adapter.in_memory_todo_tasks_repository import InMemoryTodoTasksRepository


def get_todo_tasks_service() -> TodoTasksService:
    repository = InMemoryTodoTasksRepository()
    return TodoTasksService(todo_tasks_repository=repository)