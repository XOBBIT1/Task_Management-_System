from pydantic import BaseModel, EmailStr


class CreateUserSchema(BaseModel):
    username: str
    name: str
    password: str
    email: EmailStr


class CreateUserResponseSchema(BaseModel):
    username: str
    name: str
    email: str
