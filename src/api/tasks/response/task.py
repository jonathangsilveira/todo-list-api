from typing import Optional

from pydantic import BaseModel

from src.domain.tasks.model.todo_task import TodoTask
from src.ext.datetime.datetime import to_timestamp_millis


class TaskResponse(BaseModel):
    uuid: str
    title: str
    status: str
    created_at: int
    last_sync_at: int
    updated_at: Optional[int]

    @staticmethod
    def from_domain(todo_task: TodoTask) -> "TaskResponse":
        return TaskResponse(
            uuid=todo_task.uuid,
            title=todo_task.title,
            status=todo_task.status,
            created_at=to_timestamp_millis(todo_task.created_at),
            last_sync_at=to_timestamp_millis(todo_task.last_sync_at),
            updated_at=to_timestamp_millis(todo_task.updated_at) if todo_task.updated_at else None
        )

class TasksResponse(BaseModel):
    tasks: list[TaskResponse] = []