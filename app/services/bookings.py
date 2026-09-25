from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.bookings import BookingsRepository
from app.repositories.rooms import RoomsRepository
from app.schemas.bookings import BookingCreateSchema as BookingCreate
from app.models.bookings import BookingsModel


class BookingService:
    def __init__(self, session: AsyncSession):
        # ШАГ 1: Инжектим сессию и инициализируем нужные репозитории
        self.session = session
        self.bookings_repo = BookingsRepository(session)
        self.rooms_repo = RoomsRepository(session)

    async def add_booking(self, user_id: int, booking_data: BookingCreate) -> BookingsModel:
        # ШАГ 2: Проверяем, существует ли запрашиваемая комната
        room = await self.rooms_repo.get_by_id(booking_data.room_id)
        if not room:
            raise ValueError("Указанная комната не найдена")

        # ШАГ 3: Проверяем доступность комнаты на эти даты (бизнес-проверка)
        overlapping_bookings = await self.bookings_repo.get_overlapping_bookings(
            room_id=booking_data.room_id,
            date_from=booking_data.date_from,
            date_to=booking_data.date_to
        )

        # Если количество броней на эти даты превышает или равно доступному количеству номеров (quantity)
        if len(overlapping_bookings) >= room.quantity:
            raise ValueError("На выбранные даты нет свободных номеров этой категории")

        # ШАГ 4: Расчет бизнес-показателей (стоимость)
        # Вычисляем количество ночей
        total_days = (booking_data.date_to - booking_data.date_from).days
        
        # Зафиксируем текущую цену за 1 ночь и итоговую сумму
        price = room.price
        total_cost = total_days * price

        # ШАГ 5: Подготовка данных для создания записи
        booking_dict = booking_data.model_dump()
        booking_dict.update({
            "user_id": user_id,
            "price": price,
            "total_cost": total_cost,
        })

        # ШАГ 6: Сохранение в БД через репозиторий и фиксация транзакции
        new_booking = await self.bookings_repo.add(booking_dict)
        await self.session.commit()

        return new_booking

        async def get_user_bookings(self, user_id: int) -> list[BookingsModel]:
            # ШАГ 7: Получение всех броней пользователя
            user_bookings = await self.bookings_repo.get_user_bookings(user_id=user_id)
            return user_bookings