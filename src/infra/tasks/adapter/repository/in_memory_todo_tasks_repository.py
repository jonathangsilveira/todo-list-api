from datetime import datetime, timezone
from typing import Optional

from src.core.exception.exceptions import NotFoundException
from src.domain.tasks.model.new_todo_task import NewTodoTask
from src.domain.tasks.model.todo_task import TodoTask
from src.domain.tasks.model.todo_task_status import TodoTaskStatus
from src.domain.tasks.repository.todo_tasks_repository import TodoTasksRepository


class InMemoryTodoTasksRepository(TodoTasksRepository):
    _tasks_by_uuid: dict[str, TodoTask] = {}

    async def get_todo_tasks_by_user(self, user_id: str) -> list[TodoTask]:
        return [todo_task for todo_task in self._tasks_by_uuid.values() if todo_task.owner_id == user_id]

    async def get_todo_task_by_uuid(self, uuid: str) -> Optional[TodoTask]:
        return self._tasks_by_uuid.get(uuid)

    async def upsert_todo_task(self, user_id: str, todo_task: NewTodoTask) -> TodoTask:
        local_todo_task = TodoTask(
            uuid=todo_task.uuid,
            title=todo_task.title,
            status=todo_task.status,
            owner_id=user_id,
            collaborator_ids=[],
            created_at=todo_task.created_at,
            updated_at=datetime.now(tz=timezone.utc),
            last_sync_at=datetime.now(tz=timezone.utc)
        )
        self._tasks_by_uuid[todo_task.uuid] = local_todo_task
        return local_todo_task

    async def mark_todo_task_as_done(self, uuid: str) -> TodoTask:
        todo_task = self._tasks_by_uuid.get(uuid)
        if not todo_task:
            raise NotFoundException(message=f"TODO task {uuid} not found!")
        todo_task.status = TodoTaskStatus.DONE
        todo_task.updated_at = datetime.now(timezone.utc)
        todo_task.last_sync_at = datetime.now(timezone.utc)
        return todo_task

    async def remove_todo_task_by_uuid(self, uuid: str) -> None:
        if uuid not in self._tasks_by_uuid:
            raise NotFoundException(message=f"TODO task {uuid} not found!")
        self._tasks_by_uuid.pop(uuid)