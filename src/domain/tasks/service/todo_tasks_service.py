from src.domain.tasks.exception.todo_task_change import TodoTaskChangeException
from src.domain.tasks.exception.todo_task_fetch import TodoTaskFetchException
from src.domain.tasks.exception.todo_task_not_found import TodoTaskNotFoundException
from src.domain.tasks.model.new_todo_task import NewTodoTask
from src.domain.tasks.model.todo_task import TodoTask
from src.domain.tasks.repository.todo_tasks_repository import TodoTasksRepository


class TodoTasksService:

    def __init__(self, todo_tasks_repository: TodoTasksRepository) -> None:
        self._todo_tasks_repository = todo_tasks_repository

    async def get_todo_tasks_by_user(self, user_id: str) -> list[TodoTask]:
        return await self._todo_tasks_repository.get_todo_tasks_by_user(user_id)

    async def get_todo_task_by_uuid(self, uuid: str) -> TodoTask:
        try:
            todo_task = await self._todo_tasks_repository.get_todo_task_by_uuid(uuid)
            if todo_task:
                return todo_task
        except Exception:
            raise TodoTaskFetchException()
        raise TodoTaskNotFoundException()

    async def add_todo_task(self, user_id: str, todo_task: NewTodoTask) -> None:
        try:
            await self._todo_tasks_repository.add_todo_task(user_id, todo_task)
        except Exception:
            raise TodoTaskChangeException()

    async def mark_todo_task_as_done(self, uuid: str) -> None:
        try:
            await self._todo_tasks_repository.mark_todo_task_as_done(uuid)
        except Exception:
            raise TodoTaskChangeException()

    async def remove_todo_task_by_uuid(self, uuid: str) -> None:
        try:
            await self._todo_tasks_repository.remove_todo_task_by_uuid(uuid)
        except Exception:
            raise TodoTaskChangeException()