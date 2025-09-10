from app.domain.user import User as UserDomain
from app.infrastructure.db.models.users import User as UserOrm


def user_to_domain(user: UserOrm) -> UserDomain:
    return UserDomain(
        id=user.id,
        telegram_id=user.telegram_id,
        username=user.username,
    )


def user_to_orm(user: UserDomain) -> UserOrm:
    return UserOrm(
        id=user.id,
        telegram_id=user.telegram_id,
        username=user.username,
    )
