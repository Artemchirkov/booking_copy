from app.repositories.users import UsersRepository
from app.schemas.users import UserCreateSchema
from app.models.users import UsersModel
from app.core.security import get_password_hash, verify_password, create_access_token


class UsersService:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo = users_repo

    async def register(self, user_data: UserCreate) -> UsersModel:
        # 1. Проверяем, существует ли уже такой email
        existing_user = await self.users_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("Пользователь с таким email уже существует")

        # 2. Хешируем пароль и готовим данные к сохранению
        hashed_password = get_password_hash(user_data.password)
        
        user_dict = user_data.model_dump()
        user_dict["hashed_password"] = hashed_password
        del user_dict["password"]

        # 3. Сохраняем в БД через репозиторий

        result = await self.users_repo.add(user_dict)
        await self.users_repo.session.commit()
        return result


    async def authenticate(self, email: str, password: str) -> str:
        # 1. Ищем пользователя в БД
        user = await self.users_repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Неверный email или пароль")

        # 2. Генерируем и возвращаем токен
        access_token = create_access_token(data={"sub": str(user.id)})
        return access_token