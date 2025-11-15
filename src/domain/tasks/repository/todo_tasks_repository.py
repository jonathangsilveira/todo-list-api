from abc import ABC, abstractmethod
from typing import Optional

from src.domain.tasks.model.new_todo_task import NewTodoTask
from src.domain.tasks.model.todo_task import TodoTask


class TodoTasksRepository(ABC):

    @abstractmethod
    async def get_todo_tasks_by_user(self, user_id: str) -> list[TodoTask]:
        pass

    @abstractmethod
    async def get_todo_task_by_uuid(self, uuid: str) -> Optional[TodoTask]:
        pass

    @abstractmethod
    async def add_todo_task(self, user_id: str, todo_task: NewTodoTask) -> TodoTask:
        pass

    @abstractmethod
    async def mark_todo_task_as_done(self, uuid: str) -> TodoTask:
        pass

    @abstractmethod
    async def remove_todo_task_by_uuid(self, uuid: str) -> None:
        pass