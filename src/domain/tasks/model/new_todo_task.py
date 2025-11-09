from dataclasses import dataclass
from datetime import datetime

from src.domain.tasks.model.todo_task_status import TodoTaskStatus


@dataclass
class NewTodoTask:
    uuid: str
    title: str
    status: TodoTaskStatus
    created_at: datetime