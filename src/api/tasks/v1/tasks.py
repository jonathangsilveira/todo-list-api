from fastapi import APIRouter
from fastapi.params import Depends, Path
from starlette import status
from starlette.responses import JSONResponse

from src.api.auth.dependencies import get_authorized_user
from src.api.tasks.dependencies import get_todo_tasks_service
from src.api.tasks.request.new_todo_task_input import NewTodoTaskInput
from src.api.tasks.response.task import TasksResponse, TaskResponse
from src.domain.tasks.exception.todo_task_change import TodoTaskChangeException
from src.domain.tasks.exception.todo_task_fetch import TodoTaskFetchException
from src.domain.tasks.exception.todo_task_not_found import TodoTaskNotFoundException
from src.domain.tasks.service.todo_tasks_service import TodoTasksService
from src.domain.user.model.user import User

router = APIRouter(
    prefix="/tasks/v1",
    tags=["Tasks"],
    dependencies=[Depends(get_authorized_user)]
)


@router.get(path="/all", status_code=status.HTTP_200_OK, response_model=TasksResponse)
async def get_all_tasks(authorized_user: User = Depends(get_authorized_user),
                        todo_tasks_service: TodoTasksService = Depends(get_todo_tasks_service)):
    try:
        todo_tasks = await todo_tasks_service.get_todo_tasks_by_user(user_id=authorized_user.uuid)
        tasks = [TaskResponse.from_domain(todo_task) for todo_task in todo_tasks]
        return TasksResponse(tasks=tasks)
    except TodoTaskChangeException:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "Error on changing todo task"
            }
        )
    except TodoTaskFetchException:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Error on fetching todo tasks"
            }
        )

@router.get(path="/task/{uuid}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def get_todo_task_by_uuid(uuid: str = Path(),
                                authorized_user: User = Depends(get_authorized_user),
                                todo_tasks_service: TodoTasksService = Depends(get_todo_tasks_service)):
    try:
        todo_task = await todo_tasks_service.get_todo_task_by_uuid(uuid=uuid)
        return TaskResponse.from_domain(todo_task)
    except TodoTaskNotFoundException:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": f"Todo task {uuid} not found!"
            }
        )
    except TodoTaskFetchException:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Error on fetching todo tasks"
            }
        )

@router.post(path="/task/new", status_code=status.HTTP_201_CREATED)
async def add_todo_task(new_todo_task_input: NewTodoTaskInput,
                        authorized_user: User = Depends(get_authorized_user),
                        todo_tasks_service: TodoTasksService = Depends(get_todo_tasks_service)):
    try:
        new_todo_task = new_todo_task_input.to_domain()
        await todo_tasks_service.add_todo_task(user_id=authorized_user.uuid, todo_task=new_todo_task)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Todo task created!"}
        )
    except TodoTaskFetchException:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Error on fetching todo tasks"
            }
        )

@router.patch(path="/task/{uuid}/done", status_code=status.HTTP_201_CREATED)
async def mark_todo_task_as_done(uuid: str = Path(),
                                 authorized_user: User = Depends(get_authorized_user),
                                 todo_tasks_service: TodoTasksService = Depends(get_todo_tasks_service)):
    try:
        await todo_tasks_service.mark_todo_task_as_done(uuid=uuid)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Todo task marked as done!"}
        )
    except TodoTaskFetchException:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Error on fetching todo tasks"
            }
        )

@router.delete(path="/task/{uuid}/remove", status_code=status.HTTP_200_OK)
async def remove_todo_task(uuid: str = Path(),
                           authorized_user: User = Depends(get_authorized_user),
                           todo_tasks_service: TodoTasksService = Depends(get_todo_tasks_service)):
    try:
        await todo_tasks_service.remove_todo_task_by_uuid(uuid=uuid)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Todo task {uuid} has been removed!"}
        )
    except TodoTaskFetchException:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Error on fetching todo tasks"
            }
        )