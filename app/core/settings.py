from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 1. Перечисляем все переменные из .env
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str = "SUPER_SECRET_KEY_CHANGE_ME_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 часа
    # 2. Формируем готовый URL для асинхронного подключения
    @property
    def DATABASE_URL(self) -> str:
        # Важно: драйвер обязательно postgresql+asyncpg://
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # 3. Указываем, откуда читать переменные
    model_config = SettingsConfigDict(env_file=".env")


# Создаём единственный экземпляр настроек
settings = Settings()