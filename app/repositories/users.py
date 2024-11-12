import logging
from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from settings.db.models import Users
from settings.db.session_to_postgres import DBSessionManager
from werkzeug.security import generate_password_hash

from schemas.users import UserUpdateRequestSchema


class UsersRepository:
    model = str

    def __init__(self):
        self.db_session_manager = DBSessionManager()
        super().__init__()

    async def create_user(self, instance: dict):
        async with self.db_session_manager.get_session() as session:
            try:
                hashed_password = generate_password_hash(instance.get("password"))
                new_user = Users(
                    name=instance.get("name"),
                    username=instance.get("username"),
                    password=hashed_password,
                    email=instance.get("email"),
                    created_at=datetime.utcnow()
                )
                session.add(new_user)
                await session.commit()  # Асинхронный коммит
                await session.refresh(new_user)  # Обновление объекта с новыми данными из базы
                return new_user
            except Exception as e:
                logging.info(f"Failed to create user: {e}")
                await session.rollback()  # Откат при ошибке

    async def get_user_by_username(self, username: str):
        async with self.db_session_manager.get_session() as session:
            try:
                query = select(Users).filter_by(username=username)
                result = await session.execute(query)  # Асинхронный запрос
                user = result.scalars().first()  # Получаем первый результат
                return user
            except NoResultFound as ex:
                logging.info(f"User not found: {ex}")
                return None

    async def get_user_by_name(self, name: str):
        async with self.db_session_manager.get_session() as session:
            try:
                query = select(Users).filter_by(name=name)
                result = await session.execute(query)  # Асинхронный запрос
                user = result.scalars().all()  # Получаем первый результат
                return user
            except NoResultFound as ex:
                logging.info(f"User not found: {ex}")
                return None

    async def get_user_by_email(self, email: str):
        async with self.db_session_manager.get_session() as session:
            try:
                query = select(Users).filter_by(email=email)
                result = await session.execute(query)  # Асинхронный запрос
                user = result.scalars().first()  # Получаем первый результат
                return user
            except NoResultFound as ex:
                logging.info(f"User not found: {ex}")
                return None

    async def update_user(self, username: str, user_update_data: UserUpdateRequestSchema):
        async with self.db_session_manager.get_session() as session:
            try:
                user = await self.get_user_by_username(username)
                if not user:
                    logging.info(f"User with username: {username} not found.")
                    return None
                if user_update_data.name is not None:
                    user.name = user_update_data.name
                if user_update_data.username is not None:
                    user.username = user_update_data.username
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user
            except Exception as ex:
                logging.error(f"Error updating user: {ex}")
                return None

    async def delete_user(self, username: str):
        async with self.db_session_manager.get_session() as session:
            try:
                query = select(Users).filter_by(username=username)
                result = await session.execute(query)
                user = result.scalars().first()

                if not user:
                    logging.info(f"User with username: {username} not found.")
                    return None
                await session.delete(user)
                await session.commit()
                return user
            except Exception as ex:
                logging.error(f"Error deleting user: {ex}")
