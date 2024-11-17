from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator, ValidationError


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


class EmailSchema(BaseModel):
    email: str
    is_change: bool = False


class ResetPasswordsSchema(BaseModel):
    secure_code: str
    password: str
    confirm_password: str

    @validator("confirm_password")
    def passwords_match(cls, confirm_password, values):
        if "password" in values and confirm_password != values["password"]:
            raise HTTPException(status_code=401, detail="Passwords do not match")
        return confirm_password

    def validate_passwords(self):
        try:
            self.dict()
        except ValidationError as e:
            raise ValueError(str(e)) from e
