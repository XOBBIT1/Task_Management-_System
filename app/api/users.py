import typing as tp

from fastapi import APIRouter, Request, HTTPException

from services import users
from schemas.users import (CreateUserSchema, CreateUserResponseSchema, GetUserResponseSchema,
                           GetUsersUsernameResponseSchema, UserUpdateRequestSchema)

user_routes = APIRouter()


@user_routes.post("/register/", status_code=201, response_model=CreateUserResponseSchema)
async def register_user(data: CreateUserSchema) -> tp.Dict[str, tp.Any]:
    user = await users.create_user_service(person=data)
    return user


@user_routes.get("/get_subscriptions/", status_code=201,
                 response_model=CreateUserResponseSchema)
async def get_subscriptions(request: Request):
    user = await users.create_user(person=request.state.username)
    return user


@user_routes.get("/get_user_by_name/{name}/", status_code=201,
                 response_model=GetUsersUsernameResponseSchema)
async def get_user_by_name(name: str) -> tp.Dict[str, tp.Any]:
    users_list = await users.get_by_name_service(name=name)
    return {"users": users_list}


@user_routes.get("/get_user_by_username/{username}/", status_code=201,
                 response_model=GetUserResponseSchema)
async def get_user_by_username(username: str):
    user = await users.get_by_username_service(username=username)
    return user


@user_routes.get("/get_user_by_email/{email}/", status_code=201,
                 response_model=GetUserResponseSchema)
async def get_user_by_email(email: str) -> tp.Dict[str, tp.Any]:
    user = await users.get_by_email_service(email=email)
    return user


@user_routes.patch("/update_user/{username}/",
                   response_model=GetUserResponseSchema)
async def patch_user(username: str, user_update: UserUpdateRequestSchema):
    updated_user = await users.update_user_service(username, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found or update failed")
    return updated_user


@user_routes.delete("/delete_user/{username}/",
                    status_code=200)
async def delete_user(username: str):
    deleted_user = await users.delete_user_service(username=username)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
