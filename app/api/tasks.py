import typing as tp

from fastapi import APIRouter, HTTPException

from app.services import tasks
from app.schemas.tasks import (CreateTasksSchema, CreateTasksResponseSchema,
                               GetTaskResponseSchema, GetTasksResponseSchema, SubscribeOnTasksSchema,
                               TaskUpdateRequestSchema, ChangeTaskStatusSchema, ChangeTaskPrioritySchema)

from app.schemas.users import GetSubscribersResponseSchema

tasks_routes = APIRouter()


@tasks_routes.post("/create_task/", status_code=201, response_model=CreateTasksResponseSchema)
async def create_task_endpoint(data: CreateTasksSchema) -> tp.Dict[str, tp.Any]:
    task = await tasks.create_task_service(task=data)
    return task


@tasks_routes.post("/subscribe_on_task/", status_code=201)
async def subscribe_on_task_endpoint(data: SubscribeOnTasksSchema):
    await tasks.subscribe_on_task_service(data=data)
    return {"detail": "You have successfully subscribed to tasks"}


@tasks_routes.get("/get_task_by_id/{task_id}/", status_code=201, response_model=GetTaskResponseSchema)
async def get_task_by_id_endpoint(task_id: int):
    user = await tasks.get_by_id_service(task_id=task_id)
    return user


@tasks_routes.get("/get_all_tasks/", status_code=201, response_model=GetTasksResponseSchema)
async def get_all_tasks_endpoint():
    tasks_list = await tasks.get_all_tasks_service()
    return {"tasks": tasks_list}


@tasks_routes.get("/get_all_subscribers/", status_code=201, response_model=GetSubscribersResponseSchema)
async def get_all_subscribers_endpoint(task_id: int):
    subscribers = await tasks.get_all_subscribers_service(task_id=task_id)
    return {"users": subscribers}


@tasks_routes.get("/get_task_by_name/{name}/", status_code=201, response_model=GetTaskResponseSchema)
async def get_task_by_name_endpoint(task_name: str):
    task = await tasks.get_by_name_service(task_name=task_name)
    return task


@tasks_routes.patch("/update_task/{task_id}/",
                    response_model=GetTaskResponseSchema)
async def patch_task_endpoint(task_id: int, task_update: TaskUpdateRequestSchema):
    updated_task = await tasks.update_task_service(task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found or update failed")
    return updated_task


@tasks_routes.patch("/change_task_status/{task_id}/",
                    response_model=GetTaskResponseSchema)
async def change_task_status_endpoint(task_id: int, task_update: ChangeTaskStatusSchema):
    updated_task = await tasks.change_task_status_service(task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found or update failed")
    return updated_task


@tasks_routes.patch("/change_task_priority/{task_id}/",
                    response_model=GetTaskResponseSchema)
async def change_task_priority_endpoint(task_id: int, task_update: ChangeTaskPrioritySchema):
    updated_task = await tasks.change_task_priority_service(task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found or update failed")
    return updated_task


@tasks_routes.delete("/delete_task/{task_id}/",
                     status_code=200)
async def delete_task_endpoint(task_id: int):
    deleted_task = await tasks.delete_task_service(task_id=task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "Task deleted successfully"}
