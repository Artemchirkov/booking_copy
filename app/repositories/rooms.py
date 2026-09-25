from datetime import date
from sqlalchemy import select, func, outerjoin
from app.repositories.base import BaseRepository
from app.models.rooms import RoomsModel
from app.models.bookings import BookingsModel


class RoomsRepository(BaseRepository[RoomsModel]):
    model = RoomsModel

    async def get_room_by_name(self, name: str) -> RoomsModel | None:
        query = select(self.model).where(self.model.name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_available_rooms(self, date_from: date, date_to: date) -> list[RoomsModel]:
        # 1. Подзапрос: считаем количество пересекающихся броней для каждой комнаты
        booked_rooms = (
            select(
                BookingsModel.room_id,
                func.count(BookingsModel.id).label("booked_count")
            )
            .where(
                BookingsModel.date_from < date_to,
                BookingsModel.date_to > date_from
            )
            .group_by(BookingsModel.room_id)
            .subquery()
        )

        # 2. Основной запрос: берем комнаты, где (quantity - booked_count) > 0
        query = (
            select(self.model)
            .outerjoin(booked_rooms, self.model.id == booked_rooms.c.room_id)
            .where(
                self.model.quantity - func.coalesce(booked_rooms.c.booked_count, 0) > 0
            )
        )

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_rooms_except_ids(self, excluded_ids: list[int]) -> list[RoomsModel]:
        """Возвращает все комнаты, кроме тех, что переданы в excluded_ids."""
        query = select(self.model)
        if excluded_ids:
            query = query.where(self.model.id.not_in(excluded_ids))
        
        result = await self.session.execute(query)
        return list(result.scalars().all())