from fastapi import APIRouter

from .users import user_routes
from .tasks import tasks_routes
from .auth import auth_routes

api_router = APIRouter(prefix='/api')

api_router.include_router(auth_routes, prefix='/auth', tags=['auth'])
api_router.include_router(user_routes, prefix='/protected/users', tags=['users'])
api_router.include_router(tasks_routes, prefix='/protected/tasks', tags=['tasks'])
