from fastapi import APIRouter

from .users import user_routes
from .tasks import tasks_routes

api_router = APIRouter(prefix='/api')

api_router.include_router(user_routes, prefix='/users', tags=['users_auth'])
api_router.include_router(tasks_routes, prefix='/tasks', tags=['tasks'])
