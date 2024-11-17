from fastapi import FastAPI

from app.api.routers import api_router
from app.middlewares.auth_middleware import AuthMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000',],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(AuthMiddleware())
