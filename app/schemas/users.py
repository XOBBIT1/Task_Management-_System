from typing import List, Optional

from pydantic import BaseModel, EmailStr


class BaseUserSchema(BaseModel):
    username: str
    name: str
    email: EmailStr


class CreateUserSchema(BaseUserSchema):
    password: str


class CreateUserResponseSchema(BaseUserSchema):
    ...


class GetUserResponseSchema(BaseUserSchema):
    id: int


class GetUsersUsernameResponseSchema(BaseModel):
    users: List[GetUserResponseSchema]


class GetSubscribersResponseSchema(BaseModel):
    users: List[BaseUserSchema]


class UserUpdateRequestSchema(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True
