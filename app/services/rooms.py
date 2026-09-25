from datetime import date
from app.repositories.rooms import RoomsRepository
from app.repositories.bookings import BookingsRepository
from app.models.rooms import RoomsModel


class RoomService:
    def __init__(
        self, 
        rooms_repo: RoomsRepository,
        bookings_repo: BookingsRepository,
    ):
        self.rooms_repo = rooms_repo

    async def get_all_rooms(self) -> list[RoomsModel]:
        """Получить вообще все комнаты без фильтрации."""
        return await self.rooms_repo.get_all()

    async def get_room_by_id(self, room_id: int) -> RoomsModel:
        """Получить детальную информацию о конкретной комнате."""
        room = await self.rooms_repo.get_by_id(room_id)
        if not room:
            raise ValueError(f"Комната с ID {room_id} не найдена")
        return room

    async def get_available_rooms( self, date_from: date, date_to: date, ) -> list[RoomsModel]:
        if date_from >= date_to: 
            raise ValueError("Дата заезда должна быть строго раньше даты выезда") 
        if date_from < date.today(): 
            raise ValueError("Нельзя забронировать комнату на прошедшие даты") 
        return await self.rooms_repo.get_available_rooms( date_from=date_from, date_to=date_to )