from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router

app = FastAPI(
    title="Booking.com Clone API",
    description="API сервиса бронирования номеров (FastAPI + PostgreSQL + SQLAlchemy 2.0)",
    version="1.0.0",
    docs_url="/docs",      # Указываем явно урл для Swagger UI
    redoc_url="/redoc",    # Альтернативная документация ReDoc
)

# Настройка CORS (разрешаем запросы с браузера/фронтенда)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # Важно для передачи Cookie с JWT токеном
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутер версии v1 с префиксом /api
app.include_router(api_v1_router, prefix="/api")


@app.get("/", include_in_schema=False)
async def root():
    """Простой healthcheck редирект или приветствие."""
    return {"status": "ok", "message": "Booking API is running. Go to /docs"}