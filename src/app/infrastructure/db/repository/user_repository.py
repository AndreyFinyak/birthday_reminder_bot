from sqlalchemy.orm import Session

from app.infrastructure.db.database import connection
from app.infrastructure.db.mappers.user import (
    UserDomain,
    user_to_domain,
    user_to_orm,
)
from app.infrastructure.db.models import User


class UserRepository:
    @connection
    def get_by_telegram_id(
        self, telegram_id: int, session: Session
    ) -> UserDomain | None:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        return user_to_domain(user) if user else None

    @connection
    def add(self, session: Session, user: UserDomain):
        if self.get_by_telegram_id(user.telegram_id, session):
            raise ValueError("User already exists")

        session.add(user_to_orm(user))
        session.commit()

    @connection
    def update(self, session: Session, user: UserDomain):
        if not self.get_by_telegram_id(telegram_id=user.telegram_id):
            raise ValueError("User does not exist")

        session.merge(user_to_orm(user))
        session.commit()

    @connection
    def delete(self, session: Session, user: UserDomain):
        if not self.get_by_telegram_id(telegram_id=user.telegram_id):
            raise ValueError("User does not exist")

        session.delete(user_to_orm(user))
        session.commit()
