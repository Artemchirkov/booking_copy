from app.repositories.base import BaseRepository
from app.models.users import UsersModel
from sqlalchemy import select

class UsersRepository(BaseRepository[UsersModel]):
    model = UsersModel
    
    async def get_user_by_email(self, email: str) -> UsersModel | None:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()