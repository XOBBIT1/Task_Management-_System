import typing as tp

from fastapi import APIRouter

from app.services import auth
from app.schemas.users import (CreateUserSchema, CreateUserResponseSchema)

from app.schemas.auth import RetrieveLogin, LoginSchema

auth_routes = APIRouter()


@auth_routes.post("/registration_user/", status_code=201, response_model=CreateUserResponseSchema)
async def register_user_endpoint(data: CreateUserSchema) -> tp.Dict[str, tp.Any]:
    user = await auth.create_user_service(person=data)
    return user


@auth_routes.post("/login/", response_model=RetrieveLogin, status_code=200)
async def login(data: LoginSchema):
    tokens = await auth.login_user_service(data=data)
    return tokens
