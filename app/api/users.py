import typing as tp

from fastapi import APIRouter, HTTPException

from app.services import users
from app.schemas.users import (GetUserResponseSchema,
                               GetUsersUsernameResponseSchema, UserUpdateRequestSchema)

from app.schemas.tasks import GetUerTasksResponseSchema
user_routes = APIRouter()


@user_routes.get("/get_user_tasks/", status_code=201,
                 response_model=GetUerTasksResponseSchema)
async def get_subscriptions_endpoint(user_id: int):
    user_tasks = await users.get_all_user_tasks_service(user_id=user_id)
    return {"tasks": user_tasks}


@user_routes.get("/get_user_by_name/{name}/", status_code=201,
                 response_model=GetUsersUsernameResponseSchema)
async def get_user_by_name_endpoint(name: str) -> tp.Dict[str, tp.Any]:
    users_list = await users.get_by_name_service(name=name)
    return {"users": users_list}


@user_routes.get("/get_user_by_username/{username}/", status_code=201,
                 response_model=GetUserResponseSchema)
async def get_user_by_username_endpoint(username: str):
    user = await users.get_by_username_service(username=username)
    return user


@user_routes.get("/get_user_by_email/{email}/", status_code=201,
                 response_model=GetUserResponseSchema)
async def get_user_by_email_endpoint(email: str) -> tp.Dict[str, tp.Any]:
    user = await users.get_by_email_service(email=email)
    return user


@user_routes.patch("/update_user/{user_id}/",
                   response_model=GetUserResponseSchema)
async def patch_user_endpoint(user_id: int, user_update: UserUpdateRequestSchema):
    updated_user = await users.update_user_service(user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found or update failed")
    return updated_user


@user_routes.delete("/delete_user/{user_id}/",
                    status_code=200)
async def delete_user_endpoint(user_id: int):
    deleted_user = await users.delete_user_service(user_id=user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
