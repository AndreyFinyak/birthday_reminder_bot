from app.domain.user import User
from app.infrastructure.db.repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: User) -> User:
        return await self.user_repository.add(user)
