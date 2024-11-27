import jwt
import typing as tp

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request

from app.settings import config_settings


async def authenticate(request: Request) -> tp.Tuple[bool, tp.Optional[str]]:
    """
    Проверяет токен авторизации и устанавливает user_id в request.state.
    Возвращает кортеж: (статус проверки, сообщение об ошибке или None).
    """
    auth_header = request.headers.get("Authorization", "")
    token_components = auth_header.split(" ")

    access_token = token_components[1]

    try:
        # Декодируем токен и проверяем его
        payload = jwt.decode(
            access_token, config_settings.token_secret_key, algorithms=[config_settings.algorithm]
        )
        if payload.get("sub") != config_settings.ACCESS_TOKEN_JWT_SUBJECT:
            return False, "Invalid token subject"

        # Устанавливаем user_id
        request.state.user_id = payload.get("id")
        return True, None
    except jwt.ExpiredSignatureError:
        return False, "Token expired"
    except jwt.InvalidTokenError:
        return False, "Invalid token"


class ApiKeyMiddleware(BaseHTTPMiddleware):
    """
    Middleware для проверки токенов доступа на определенных маршрутах.
    """
    authorize_paths = [
        '/docs',
        '/openapi.json',
        '/api/auth/login/',
        '/api/auth/registration_user/',
    ]

    async def dispatch(self, request: Request, call_next: tp.Any) -> tp.Any:
        print(request.url.path)
        if request.url.path not in self.authorize_paths and request.method != "OPTIONS":
            is_valid, error_message = await authenticate(request)
            if not is_valid:
                return JSONResponse(
                    content={"error": error_message}, status_code=401
                )
        request.state.user_id = getattr(request.state, "user_id", None)
        return await call_next(request)
