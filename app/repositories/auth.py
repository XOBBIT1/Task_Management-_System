import typing as tp
import jwt

from datetime import timedelta, datetime
from app.schemas.auth import ObtainTokenResponseSchema
from app.settings.config_settings import (token_secret_key, algorithm,
                                          access_token_expire_minutes, refresh_token_expire_days)

TOKEN_CREATE_HELPING_DATA: tp.Dict[str, tp.Any] = {
    'refresh': {
        'expire': refresh_token_expire_days,
        'subject': 'refresh'
    },
    'access': {
        'expire': access_token_expire_minutes,
        'subject': "access"
    }
}


class AuthRepository:

    def __init__(self):
        self.secret_key = token_secret_key
        self.token_algorithm = algorithm
        self.access_token_expire = int(access_token_expire_minutes)
        self.refresh_token_expire = int(refresh_token_expire_days)
        super().__init__()

    async def create_token(self, token_type: str, user_id: str) -> str:
        """ Create a single access or refresh token """

        expire = datetime.utcnow() + timedelta(minutes=float(TOKEN_CREATE_HELPING_DATA[token_type]['expire']))

        payload = {
            'id': user_id,
            'exp': expire,
            'sub': TOKEN_CREATE_HELPING_DATA[token_type]['subject'],
        }

        encoded_jwt = jwt.encode(payload=payload, key=self.secret_key, algorithm=self.token_algorithm)
        return encoded_jwt

    async def create_tokens(self, user_id: str) -> ObtainTokenResponseSchema:
        """ Create access and refresh tokens """

        access_token = await self.create_token(token_type='access', user_id=user_id)
        refresh_token = await self.create_token(token_type='refresh', user_id=user_id)

        return_data: tp.Dict[str, tp.Any] = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "access_token_expire": self.access_token_expire,
            "refresh_token_expire": self.refresh_token_expire,
        }
        return ObtainTokenResponseSchema(**return_data)
