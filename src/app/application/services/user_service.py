from app.domain.user import User
from app.infrastructure.db.repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def add(
        self,
        chat_id: int,
        username: str,
        first_name: str,
        last_name: str,
    ) -> User:
        user = User(
            chat_id=chat_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        await self.user_repository.add(user)

        return user
