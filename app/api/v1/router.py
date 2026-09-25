from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.rooms import router as rooms_router
from app.api.v1.endpoints.bookings import router as bookings_router

api_v1_router = APIRouter(prefix="/v1")

# Объединяем все изолированные эндпоинты в один роутер v1
api_v1_router.include_router(auth_router)
api_v1_router.include_router(rooms_router)
api_v1_router.include_router(bookings_router)