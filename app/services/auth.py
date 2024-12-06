from fastapi import HTTPException

from passlib.context import CryptContext
from starlette.responses import JSONResponse

from app.repositories.users import UsersRepository

from app.repositories.auth import AuthRepository
from app.schemas.auth import RetrieveLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user_service(person) -> dict:
    user_username = await UsersRepository().get_user_by_username(username=person.username)
    user_email = await UsersRepository().get_user_by_email(email=person.email)
    if user_username:
        raise HTTPException(
            status_code=409, detail="User with such username already exists"
        )
    elif user_email:
        raise HTTPException(
            status_code=409, detail="User with such email already exists"
        )
    return await UsersRepository().create_user(instance=person.dict())


async def login_user_service(data) -> JSONResponse:
    user = await UsersRepository().get_user_by_email(email=data.email)
    if user is None:
        raise HTTPException(status_code=404, detail="No such user with chosen email.")

    if not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect credentials.")

    tokens = await AuthRepository().create_tokens(user_id=user.id)
    user_dict = {
        "id": user.id,
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at,
        "is_verified": user.is_verified,
    }
    response_content = RetrieveLogin(user=user_dict, **tokens.dict())
    response = JSONResponse(content=response_content.dict())
    return response


async def get_user_by_token(self, authorization: str) -> dict:
    user_id = await self.tokens.decode_access_jwt_token(authorization=authorization)
    return await self.get_user_by_id(user_id=user_id)
