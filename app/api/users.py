import logging

from fastapi import APIRouter, Request, HTTPException, status


user_routes = APIRouter()


@user_routes.post("/register/", status_code=201)
async def register_private_person(request: Request):
    try:
        data = await request.json()  # Получаем JSON-данные из запроса
        return data  # Здесь вы можете обработать данные, например, сохранить их в базе данных
    except Exception as e:
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data format")
