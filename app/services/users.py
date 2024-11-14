from fastapi import HTTPException

from repositories.users import UsersRepository

from schemas.users import UserUpdateRequestSchema

from repositories.tasks import TasksRepository


async def create_user_service(person) -> dict:
    user_username = await UsersRepository().get_user_by_username(username=person.username)
    user_email = await UsersRepository().get_user_by_email(email=person.email)
    if user_email or user_username:
        raise HTTPException(
            status_code=409, detail="User with such username already exists"
        )
    return await UsersRepository().create_user(instance=person.dict())


async def get_by_username_service(username):
    user = await UsersRepository().get_user_by_username(username=username)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=409, detail="User with such username doesn't exist"
        )


async def get_by_name_service(name):
    user = await UsersRepository().get_user_by_name(name=name)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=409, detail="User with such name doesn't exist"
        )


async def get_by_email_service(email):
    user = await UsersRepository().get_user_by_email(email=email)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=409, detail="User with such name doesn't exist"
        )


async def update_user_service(user_id: int, user_update_data: UserUpdateRequestSchema):
    user = await UsersRepository().get_user_by_email(email=user_update_data.email)
    if user:
        return await UsersRepository().update_user(user_id, user_update_data)
    else:
        raise HTTPException(
            status_code=409, detail="User with such name doesn't exist"
        )


async def get_all_user_tasks_service(user_id: int):
    user_tasks = await UsersRepository().get_all_user_tasks(TasksRepository(), user_id)
    if user_tasks:
        return user_tasks
    else:
        raise HTTPException(
            status_code=409, detail="You don't have any tasks yet"
        )


async def delete_user_service(user_id: int):
    user = await UsersRepository().get_user_by_id(user_id=user_id)
    if user:
        return await UsersRepository().delete_user(user_id)
    else:
        raise HTTPException(
            status_code=409, detail="User with such name doesn't exist"
        )
