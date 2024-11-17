import jwt
from starlette.responses import JSONResponse
from fastapi import Request
from app.settings.config_settings import token_secret_key, algorithm


class AuthMiddleware:
    async def __call__(self, request: Request, call_next):
        if request.url.path.startswith("/api/protected/"):
            token = request.cookies.get("access_token")
            if not token:
                return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

            try:
                payload = jwt.decode(token, token_secret_key, algorithms=[algorithm])
                request.state.user_id = payload["id"]
            except jwt.ExpiredSignatureError:
                return JSONResponse(status_code=401, content={"detail": "Token expired"})
            except jwt.InvalidTokenError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        response = await call_next(request)
        return response
