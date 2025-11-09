from typing import Optional

from pydantic import BaseModel

from src.domain.tasks.model.todo_task import TodoTask


class TaskResponse(BaseModel):
    uuid: str
    title: str
    status: str
    created_at: str
    updated_at: str
    last_sync_at: Optional[str]

    @staticmethod
    def from_domain(todo_task: TodoTask) -> "TaskResponse":
        return TaskResponse(
            uuid=todo_task.uuid,
            title=todo_task.title,
            status=todo_task.status,
            created_at=str(todo_task.created_at),
            updated_at=str(todo_task.updated_at),
            last_sync_at=str(todo_task.last_sync_at) if todo_task.last_sync_at else None
        )

class TasksResponse(BaseModel):
    tasks: list[TaskResponse] = []