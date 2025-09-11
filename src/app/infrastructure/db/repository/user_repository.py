from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.infrastructure.db.database import connection
from app.infrastructure.db.mappers.user import (
    UserDomain,
    user_to_domain,
    user_to_orm,
)
from app.infrastructure.db.models import User


class UserRepository:
    @connection
    async def add(
        self, user: UserDomain, session: AsyncSession
    ) -> UserDomain | None:
        existing = await self.get_by_chat_id(chat_id=user.chat_id)

        if existing:
            return None

        orm_user = user_to_orm(user=user)

        session.add(orm_user)
        await session.commit()
        await session.refresh(orm_user)

        return user_to_domain(user=orm_user)

    @connection
    async def get_by_chat_id(
        self, chat_id: int, session: AsyncSession
    ) -> UserDomain | None:
        result = await session.execute(
            select(User).where(User.chat_id == chat_id)
        )
        orm_user = result.scalars().first()
        return user_to_domain(orm_user) if orm_user else None

    @connection
    async def list_all(self, session: AsyncSession) -> list[UserDomain]:
        result = await session.execute(select(User))
        return [user_to_domain(orm) for orm in result.scalars().all()]

    @connection
    async def update(
        self, chat_id: int, session: AsyncSession, **kwargs
    ) -> UserDomain | None:
        await session.execute(
            sqlalchemy_update(User)
            .where(User.chat_id == chat_id)
            .values(**kwargs)
        )
        await session.commit()
        return await self.get_by_chat_id(chat_id)

    @connection
    async def delete(self, chat_id: int, session: AsyncSession) -> None:
        await session.execute(
            sqlalchemy_delete(User).where(User.chat_id == chat_id)
        )
        await session.commit()
