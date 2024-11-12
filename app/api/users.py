import typing as tp

from fastapi import APIRouter

from services import users
from schemas.users import CreateUserSchema, CreateUserResponseSchema

user_routes = APIRouter()


@user_routes.post("/register/", status_code=201, response_model=CreateUserResponseSchema)
async def register_user(data: CreateUserSchema) -> tp.Dict[str, tp.Any]:
    user = await users.create_user(person=data)
    return user


@user_routes.get("/get_subscriptions/", status_code=201, response_model=CreateUserResponseSchema)
async def get_subscriptions(data: CreateUserSchema) -> tp.Dict[str, tp.Any]:
    user = await users.create_user(person=data)
    return user


@user_routes.get("/get_user_by_name/", status_code=201, response_model=CreateUserResponseSchema)
async def get_user_by_name(data: CreateUserSchema) -> tp.Dict[str, tp.Any]:
    user = await users.create_user(person=data)
    return user


@user_routes.get("/get_user_by_username/", status_code=201, response_model=CreateUserResponseSchema)
async def get_user_by_username(data: CreateUserSchema) -> tp.Dict[str, tp.Any]:
    user = await users.create_user(person=data)
    return user


@user_routes.get("/get_user_by_email/", status_code=201, response_model=CreateUserResponseSchema)
async def get_user_by_email(data: CreateUserSchema) -> tp.Dict[str, tp.Any]:
    user = await users.create_user(person=data)
    return user


@user_routes.put("/put_data/", status_code=201, response_model=CreateUserResponseSchema)
async def put_data(data: CreateUserSchema) -> tp.Dict[str, tp.Any]:
    user = await users.create_user(person=data)
    return user


@user_routes.delete("/delete_user/", status_code=201, response_model=CreateUserResponseSchema)
async def delete_user(data: CreateUserSchema) -> tp.Dict[str, tp.Any]:
    user = await users.create_user(person=data)
    return user
