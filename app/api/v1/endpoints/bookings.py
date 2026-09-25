from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.bookings import BookingCreateSchema, BookingReadSchema
from app.services.bookings import BookingService
from app.models.users import UsersModel
from app.api.dependencies import get_booking_service, get_current_user

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get(
    "/me", 
    response_model=list[BookingReadSchema],
    summary="Получить все бронирования текущего залогиненного пользователя"
)
async def get_my_bookings(
    current_user: UsersModel = Depends(get_current_user),
    booking_service: BookingService = Depends(get_booking_service),
):
    return await booking_service.get_user_bookings(user_id=current_user.id)


@router.post(
    "", 
    response_model=BookingReadSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Забронировать номер"
)
async def create_booking(
    booking_data: BookingCreateSchema,
    current_user: UsersModel = Depends(get_current_user),
    booking_service: BookingService = Depends(get_booking_service),
):
    try:
        booking = await booking_service.add_booking(
            user_id=current_user.id, 
            booking_data=booking_data
        )
        return booking
    except ValueError as e:
        # Ловим ошибки бизнес-логики (например: "Комната уже занята на эти даты")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )


@router.delete(
    "/{booking_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Отменить бронирование"
)
async def cancel_booking(
    booking_id: int,
    current_user: UsersModel = Depends(get_current_user),
    booking_service: BookingService = Depends(get_booking_service),
):
    try:
        await booking_service.cancel_booking(
            booking_id=booking_id, 
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )