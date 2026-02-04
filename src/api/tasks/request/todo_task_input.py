import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel

from src.domain.tasks.model.new_todo_task import NewTodoTask
from src.domain.tasks.model.todo_task_status import TodoTaskStatus
from src.ext.datetime.datetime import from_timestamp_millis_utc


class TodoTaskInput(BaseModel):
    title: str
    status: Optional[Literal['PENDING', 'DONE', 'REMOVED']] = "PENDING"
    uuid: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None

    def to_domain(self) -> NewTodoTask:
        return NewTodoTask(
            title=self.title,
            status=TodoTaskStatus(value=self.status),
            uuid=self.uuid or str(uuid.uuid4()),
            created_at=from_timestamp_millis_utc(self.created_at) or datetime.now(timezone.utc),
            updated_at=from_timestamp_millis_utc(self.updated_at) if self.updated_at else None
        )
