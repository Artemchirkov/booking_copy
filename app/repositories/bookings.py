from app.repositories.base import BaseRepository
from app.models.bookings import BookingsModel
from sqlalchemy import select
from datetime import date

class BookingsRepository(BaseRepository[BookingsModel]):
    model = BookingsModel

    async def get_overlapping_bookings(self, room_id: int, date_from: date, date_to: date) -> list[BookingsModel]:
        query = select(self.model).where(
            self.model.room_id == room_id,
            self.model.date_from < date_to,
            self.model.date_to > date_from
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_user_bookings(self, user_id: int) -> list[BookingsModel]:
        query = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .options(joinedload(self.model.room)) # Чтобы Pydantic не упал при сериализации
    )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_booked_room_ids(self, date_from: date, date_to: date) -> list[int]:
        """Возвращает список ID комнат, у которых есть пересечения по датам с указанным диапазоном."""
        query = select(self.model.room_id).where(
            self.model.date_from < date_to,
            self.model.date_to > date_from,
        )
        result = await self.session.execute(query)
        # scalar_one_or_none / scalars().all() отдаст простой список [1, 3, 5]
        return list(result.scalars().all())
