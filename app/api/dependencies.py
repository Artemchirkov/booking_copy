from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.bookings import BookingService
from app.db.database import async_session_maker
from app.core.security import decode_access_token
from app.repositories.users import UsersRepository
from app.models.users import UsersModel
from app.services.rooms import RoomService

# OAuth2 схема с эндпоинтом получения токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Генератор сессии БД
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Функция для получения асинхронной сессии SQLAlchemy.
    Используется в качестве зависимости в FastAPI.
    """
    async with async_session_maker() as session:
        yield session


# Alias-типы для чистоты кода
DBDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(token: TokenDep, session: DBDep) -> UsersModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось валидировать учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise credentials_exception

    user = await UsersRepository(session).get_by_id(int(user_id))
    if not user:
        raise credentials_exception

    return user

    from fastapi import Depends


def get_booking_service(
    session: AsyncSession = Depends(get_db)
) -> BookingService:
    """Собирает BookingService и прокидывает в него асинхронную сессию."""
    return BookingService(session)

async def get_room_service(session: DBDep = Depends(get_db)) -> RoomService:
    rooms_repo = RoomsRepository(session)
    return RoomService(rooms_repo)




# Тип для использования в защищённых роутах
CurrentUserDep = Annotated[UsersModel, Depends(get_current_user)]