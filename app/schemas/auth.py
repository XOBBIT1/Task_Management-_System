
from pydantic import BaseModel, Field


class BaseAuthSchema(BaseModel):
    access_token: str
    refresh_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class AccessToken(RefreshToken):
    access_token: str


class Token(AccessToken):
    ...


class BaseAuthRead(BaseModel):
    id: int
    name: str
    username: str
    email: str
    is_verified: bool


class RetrieveLogin(Token):
    user: BaseAuthRead


class LoginSchema(BaseModel):
    email: str
    password: str


class ObtainTokenResponseSchema(BaseModel):
    access_token: str = Field(description='Access token')
    refresh_token: str = Field(description='Refresh token')
    access_token_expire: int = Field(description='Access token expire time in minutes')
    refresh_token_expire: int = Field(description='Refresh token expire time in minutes')
