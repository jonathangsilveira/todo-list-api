import datetime

from src.domain.tasks.model.new_todo_task import NewTodoTask
from src.domain.tasks.model.todo_task import TodoTask
from src.domain.tasks.model.todo_task_status import TodoTaskStatus
from src.infra.database.sqlite.model.sqlite_models import TodoTaskEntity


class EntityTodoTaskMapper:

    @staticmethod
    def new_entity(todo_task_creation: NewTodoTask, owner_id: str) -> TodoTaskEntity:
        return TodoTaskEntity(
            id=todo_task_creation.uuid,
            title=todo_task_creation.title,
            status=todo_task_creation.status.value(),
            owner_id=owner_id,
            created_at=todo_task_creation.created_at,
            last_sync_at=datetime.datetime.now(tz=datetime.timezone.utc)
        )

    @staticmethod
    def from_entity(todo_task_entity: TodoTaskEntity) -> TodoTask:
        return TodoTask(
            uuid=todo_task_entity.id,
            title=todo_task_entity.title,
            status=TodoTaskStatus(todo_task_entity.status),
            created_at=todo_task_entity.created_at,
            updated_at=todo_task_entity.updated_at,
            last_sync_at=todo_task_entity.last,
            owner_id=todo_task_entity.owner_id,
            collaborator_ids=[]
        )

    @staticmethod
    def to_entity(todo_task: TodoTask) -> TodoTaskEntity:
        return TodoTaskEntity(
            id=todo_task.uuid,
            title=todo_task.title,
            status=todo_task.status.value(),
            owner_id=todo_task.owner_id,
            created_at=todo_task.created_at,
            updated_at=todo_task.updated_at,
            last_sync_at=todo_task.last_sync_at
        )