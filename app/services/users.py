from fastapi import HTTPException

from repositories.users import UsersRepository


async def create_user(person) -> dict:
    user = await UsersRepository().get_user_by_username(username=person.username)
    if user:
        raise HTTPException(
            status_code=409, detail="User with such username already exists"
        )
    return await UsersRepository().create_user(instance=person.dict())
