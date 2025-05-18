import contextlib
import logging
from datetime import datetime
from typing import Annotated, AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, mapped_column

Base = declarative_base()

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True, index=True)]


class DatabaseSessionManager:
    """Manages database sessions with a singleton pattern"""
    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.sessionmaker: async_sessionmaker | None = None

    def init(self, dsn: str):
        self.engine = create_async_engine(dsn)
        self.sessionmaker = async_sessionmaker(autocommit=False, bind=self.engine)

    async def close(self):
        if self.engine is None:
            logging.error("DatabaseSessionManager is not initialized")
            raise DatabaseSessionException()

        await self.engine.dispose()
        self.engine = None
        self.sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.engine is None:
            logging.error("DatabaseSessionManager is not initialized")
            raise DatabaseSessionException()

        async with self.engine.begin() as connection:
            try:
                yield connection

            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self.sessionmaker is None:
            logging.error("DatabaseSessionManager is not initialized")
            raise DatabaseSessionException()

        session = self.sessionmaker()
        try:
            yield session

        except Exception:
            await session.rollback()
            raise

        finally:
            await session.close()


sessionmanager = DatabaseSessionManager()


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session


class DatabaseSessionException(Exception):
    def __init__(self, message="DatabaseSessionManager is not initialized"):
        self.message = message
        super().__init__(self.message)
