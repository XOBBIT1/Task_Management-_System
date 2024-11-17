import typing as tp

from fastapi import APIRouter, HTTPException, Request

from app.services import users, email
from app.schemas.users import (GetUserResponseSchema, GetUsersUsernameResponseSchema,
                               UserUpdateRequestSchema, EmailSchema, ResetPasswordsSchema)

from app.schemas.tasks import GetUerTasksResponseSchema
user_routes = APIRouter()


@user_routes.get("/get_user_tasks/", status_code=201,
                 response_model=GetUerTasksResponseSchema)
async def get_subscriptions_endpoint(request: Request):
    user_tasks = await users.get_all_user_tasks_service(user_id=request.state.user_id)
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
async def get_user_by_email_endpoint(email_data: str) -> tp.Dict[str, tp.Any]:
    user = await users.get_by_email_service(email=email_data)
    return user


@user_routes.patch("/update_user/",
                   response_model=GetUserResponseSchema)
async def patch_user_endpoint(request: Request, user_update: UserUpdateRequestSchema):
    updated_user = await users.update_user_service(request.state.user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found or update failed")
    return updated_user


@user_routes.delete("/delete_user/",
                    status_code=200)
async def delete_user_endpoint(request: Request):
    deleted_user = await users.delete_user_service(user_id=request.state.user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}


@user_routes.post("/forgot_password/", status_code=200)
async def forgot_password(email_data: EmailSchema):
    await email.forgot_password(email=email_data)
    return {"detail": "Successfully sended email"}


@user_routes.post("/reset_password/", status_code=200)
async def reset_password(data: ResetPasswordsSchema):
    await email.reset_password_service(data=data)
    return {"detail": "Successfully changed password"}
