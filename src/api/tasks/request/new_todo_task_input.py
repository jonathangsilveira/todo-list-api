import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel

from src.domain.tasks.model.new_todo_task import NewTodoTask
from src.domain.tasks.model.todo_task_status import TodoTaskStatus


class NewTodoTaskInput(BaseModel):
    title: str
    status: Optional[Literal['PENDING', 'DONE', 'REMOVED']] = "PENDING"
    uuid: Optional[str] = None
    created_at: Optional[datetime] = None

    def to_domain(self) -> NewTodoTask:
        return NewTodoTask(
            title=self.title,
            status=TodoTaskStatus(value=self.status),
            uuid=self.uuid or str(uuid.uuid4()),
            created_at=self.created_at or datetime.now(timezone.utc)
        )
