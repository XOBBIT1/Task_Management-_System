from fastapi import HTTPException

from app.repositories.users import UsersRepository

from app.schemas.users import UserUpdateRequestSchema

from app.repositories.tasks import TasksRepository


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
