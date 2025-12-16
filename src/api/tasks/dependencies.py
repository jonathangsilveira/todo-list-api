from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.dependency_injection.dependency_container import DependencyContainer
from src.domain.tasks.service.todo_tasks_service import TodoTasksService


@inject
def get_todo_tasks_service(
        todo_task_service: TodoTasksService = Depends(Provide[DependencyContainer.todo_tasks_service])
) -> TodoTasksService:
    return todo_task_service
