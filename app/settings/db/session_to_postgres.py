from app.settings import config_settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


class DBSessionManager:
    def __init__(self,):
        self._engine = create_async_engine(config_settings.db_url, echo=True)
        self._AsyncSession = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    # Асинхронный контекстный менеджер для сессии
    class SessionContextManager:
        def __init__(self, sessionmaker: sessionmaker):
            self._sessionmaker = sessionmaker
            self._session = None

        async def __aenter__(self):
            self._session = self._sessionmaker()
            return self._session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                await self._session.rollback()
            await self._session.close()

    def get_session(self):
        return self.SessionContextManager(self._AsyncSession)
