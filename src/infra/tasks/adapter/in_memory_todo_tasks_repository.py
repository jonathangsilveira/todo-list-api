from datetime import datetime, timezone
from typing import Optional

from src.domain.tasks.model.new_todo_task import NewTodoTask
from src.domain.tasks.model.todo_task import TodoTask
from src.domain.tasks.model.todo_task_status import TodoTaskStatus
from src.domain.tasks.repository.todo_tasks_repository import TodoTasksRepository


class InMemoryTodoTasksRepository(TodoTasksRepository):
    _tasks_by_user: dict[str, list[TodoTask]] = {}
    _tasks_by_uuid: dict[str, TodoTask] = {}

    async def get_todo_tasks_by_user(self, user_id: str) -> list[TodoTask]:
        return self._tasks_by_user.get(user_id, [])

    async def get_todo_task_by_uuid(self, uuid: str) -> Optional[TodoTask]:
        return self._tasks_by_uuid.get(uuid)

    async def add_todo_task(self, user_id: str, todo_task: NewTodoTask) -> None:
        todo_tasks = self._tasks_by_user.get(user_id, [])
        local_todo_task = TodoTask(
            uuid=todo_task.uuid,
            title=todo_task.title,
            status=todo_task.status,
            owner_id=user_id,
            collaborator_ids=[],
            created_at=todo_task.created_at,
            updated_at=todo_task.created_at,
            last_sync_at=None
        )
        self._tasks_by_uuid[todo_task.uuid] = local_todo_task
        todo_tasks.append(local_todo_task)
        self._tasks_by_user[user_id] = todo_tasks

    async def mark_todo_task_as_done(self, uuid: str) -> None:
        todo_task = self._tasks_by_uuid.get(uuid)
        if not todo_task:
            return
        todo_task.status = TodoTaskStatus.DONE
        todo_task.updated_at = datetime.now(timezone.utc)
        todo_task.last_sync_at = datetime.now(timezone.utc)
        for todo_tasks in self._tasks_by_user.values():
            for task in todo_tasks:
                if task.uuid == uuid:
                    task.status = todo_task.status
                    task.updated_at = todo_task.updated_at
                    task.last_sync_at = todo_task.last_sync_at
                    break

    async def remove_todo_task_by_uuid(self, uuid: str) -> None:
        if uuid in self._tasks_by_uuid:
            return
        self._tasks_by_uuid.pop(uuid)
        for todo_tasks in self._tasks_by_user.values():
            for task in todo_tasks:
                if task.uuid == uuid:
                    todo_tasks.remove(task)
                    break