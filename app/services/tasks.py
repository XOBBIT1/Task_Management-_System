from fastapi import HTTPException

from app.repositories.tasks import TasksRepository
from app.repositories.users import UsersRepository
from app.schemas.tasks import TaskUpdateRequestSchema


async def create_task_service(task, creator_id: int) -> dict:
    task_username = await TasksRepository().get_task_by_task_name(task_name=task.task_name)
    if task_username:
        raise HTTPException(
            status_code=409, detail="User with such task_username already exists"
        )
    return await TasksRepository().create_task(instance=task.dict(), creator_id=creator_id)


async def get_all_tasks_service():
    tasks = await TasksRepository().get_all_tasks()
    if tasks:
        return tasks
    else:
        raise HTTPException(
            status_code=409, detail="You don't have any tasks yet"
        )


async def get_all_subscribers_service(task_id: int):
    subscribers = await TasksRepository().get_all_subscribers(UsersRepository(), task_id)
    if subscribers:
        return subscribers
    else:
        raise HTTPException(
            status_code=409, detail="You don't have any subscribers yet"
        )


async def get_by_name_service(task_name):
    task = await TasksRepository().get_task_by_task_name(task_name=task_name)
    if task:
        return task
    else:
        raise HTTPException(
            status_code=409, detail="User with such name doesn't exist"
        )


async def get_by_id_service(task_id: int):
    task = await TasksRepository().get_task_by_id(task_id=task_id)
    if task:
        return task
    else:
        raise HTTPException(
            status_code=409, detail=f"Task with such id: {task_id} doesn't exist"
        )


async def subscribe_on_task_service(task_id, sub_id) -> dict:
    task = await TasksRepository().get_task_by_id(task_id=task_id)
    if task:
        return await TasksRepository().subscribe_on_task(task_id=task_id, sub_id=sub_id)
    else:
        raise HTTPException(
            status_code=409, detail=f"Task with such id: {task_id} doesn't exist"
        )


async def update_task_service(task_id, task_update_data: TaskUpdateRequestSchema):
    task = await TasksRepository().get_task_by_id(task_id=task_id)
    if task:
        return await TasksRepository().update_task(task_id, task_update_data)
    else:
        raise HTTPException(
            status_code=409, detail=f"Task with such id:{task_id} doesn't exist"
        )


async def delete_task_service(task_id):
    user = await TasksRepository().get_task_by_id(task_id=task_id)
    if user:
        return await TasksRepository().delete_task(task_id)
    else:
        raise HTTPException(
            status_code=409, detail="Task with such name doesn't exist"
        )
