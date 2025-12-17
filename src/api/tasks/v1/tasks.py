from fastapi import APIRouter
from fastapi.params import Depends, Path
from starlette import status
from starlette.responses import JSONResponse

from src.api.auth.dependencies import get_authorized_user
from src.api.tasks.dependencies import get_todo_tasks_service
from src.api.tasks.request.new_todo_task_input import NewTodoTaskInput
from src.api.tasks.response.task import TasksResponse, TaskResponse
from src.domain.tasks.service.todo_tasks_service import TodoTasksService
from src.domain.user.model.user_models import User

router = APIRouter(
    prefix="/tasks/v1",
    tags=["Tasks"],
    dependencies=[Depends(get_authorized_user)]
)


@router.get(path="/all", status_code=status.HTTP_200_OK, response_model=TasksResponse)
async def get_all_tasks(authorized_user: User = Depends(get_authorized_user),
                        todo_tasks_service: TodoTasksService = Depends(get_todo_tasks_service)):
    todo_tasks = await todo_tasks_service.get_todo_tasks_by_user(user_id=authorized_user.id)
    response = TasksResponse(tasks=[TaskResponse.from_domain(task) for task in todo_tasks])
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response.model_dump(exclude_none=True)
    )


@router.get(path="/task/{uuid}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def get_todo_task_by_uuid(todo_task_uuid: str = Path(alias="uuid"),
                                authorized_user: User = Depends(get_authorized_user),
                                todo_tasks_service: TodoTasksService = Depends(get_todo_tasks_service)):
    todo_task = await todo_tasks_service.get_todo_task_by_uuid(uuid=todo_task_uuid)
    response = TaskResponse.from_domain(todo_task)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response.model_dump(exclude_none=True)
    )


@router.post(path="/task/new", status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def add_todo_task(new_todo_task_input: NewTodoTaskInput,
                        authorized_user: User = Depends(get_authorized_user),
                        todo_tasks_service: TodoTasksService = Depends(get_todo_tasks_service)):
    new_todo_task = new_todo_task_input.to_domain()
    created_task = await todo_tasks_service.upsert_todo_task(user_id=authorized_user.id, todo_task=new_todo_task)
    response = TaskResponse.from_domain(created_task)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response.model_dump(exclude_none=True)
    )

@router.patch(path="/task/{uuid}/done", status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def mark_todo_task_as_done(todo_task_uuid: str = Path(alias="uuid"),
                                 authorized_user: User = Depends(get_authorized_user),
                                 todo_tasks_service: TodoTasksService = Depends(get_todo_tasks_service)):
    updated_task = await todo_tasks_service.mark_todo_task_as_done(uuid=todo_task_uuid)
    response = TaskResponse.from_domain(updated_task)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response.model_dump(exclude_none=True)
    )


@router.delete(path="/task/{uuid}/remove", status_code=status.HTTP_204_NO_CONTENT)
async def remove_todo_task(todo_task_uuid: str = Path(alias="uuid"),
                           authorized_user: User = Depends(get_authorized_user),
                           todo_tasks_service: TodoTasksService = Depends(get_todo_tasks_service)):
    await todo_tasks_service.remove_todo_task_by_uuid(uuid=todo_task_uuid)