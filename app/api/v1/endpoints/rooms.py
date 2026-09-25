from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.rooms import RoomReadSchema as RoomRead
from app.services.rooms import RoomService
from app.api.dependencies import get_room_service

router = APIRouter(prefix="/rooms", tags=["Комнаты и Поиск"])


@router.get(
    "", 
    response_model=list[RoomRead],
    summary="Получить список всех свободных комнат на выбранный период"
)
async def get_available_rooms(
    date_from: date,
    date_to: date,
    room_service: RoomService = Depends(get_room_service),
):
    try:
        rooms = await room_service.get_available_rooms(
            date_from=date_from, 
            date_to=date_to
        )
        return rooms
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )


@router.get(
    "/{room_id}", 
    response_model=RoomRead,
    summary="Получить подробную информацию о конкретном номере"
)
async def get_room_by_id(
    room_id: int,
    room_service: RoomService = Depends(get_room_service),
):
    try:
        return await room_service.get_room_by_id(room_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )