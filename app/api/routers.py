from fastapi import APIRouter

from .users import user_routes

api_router = APIRouter(prefix='/api')

api_router.include_router(user_routes, prefix='/users', tags=['users_auth'])
