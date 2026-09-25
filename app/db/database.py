from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.settings import settings
from typing import AsyncGenerator

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,  # Включает логирование SQL-запросов в консоль (удобно при разработке)
)
    
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Отключает очистку объектов после commit, чтобы не делать лишних повторных запросов
)

