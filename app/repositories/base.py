from typing import Generic, TypeVar, Type, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import Base  # твой базовый класс моделей

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    model: Type[ModelType]  

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, model_id: int) -> ModelType | None:
        query = select(self.model).filter_by(id=model_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, **filter_by: Any) -> list[ModelType]:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def add(self, **data: Any) -> ModelType:
        instance = self.model(**data)
        self.session.add(instance)
        return instance