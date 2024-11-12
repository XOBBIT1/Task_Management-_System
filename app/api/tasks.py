import typing as tp

from fastapi import APIRouter

from services import users
from schemas.users import CreateUserSchema, CreateUserResponseSchema

tasks_routes = APIRouter()


@tasks_routes.post("/create_task/", status_code=201, response_model=CreateUserResponseSchema)
async def register_private_person(data: CreateUserSchema) -> tp.Dict[str, tp.Any]:
    user = await users.create_user(person=data)
    return user
