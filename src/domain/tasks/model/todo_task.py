from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from src.domain.tasks.model.todo_task_status import TodoTaskStatus


@dataclass
class TodoTask:
    uuid: str
    title: str
    status: TodoTaskStatus
    owner_id: str
    collaborator_ids: list[str]
    created_at: datetime
    updated_at: datetime
    last_sync_at: Optional[datetime]