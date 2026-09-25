from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.rooms import RoomsModel
    from app.models.users import UserModel


class BookingsModel(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # 1. Внешние ключи (для колонки в базе данных)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # Даты и финансы
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    total_cost: Mapped[int] = mapped_column(Integer, nullable=False)

    # 2. ORM-связи (для удобной работы в Python)
    room: Mapped["RoomsModel"] = relationship(back_populates="bookings")
    user: Mapped["UsersModel"] = relationship(back_populates="bookings")