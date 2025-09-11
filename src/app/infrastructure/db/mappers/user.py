from app.domain.user import User as UserDomain
from app.infrastructure.db.models.users import User as UserOrm


def user_to_domain(user: UserOrm) -> UserDomain:
    return UserDomain(
        first_name=user.first_name,
        last_name=user.last_name,
        chat_id=user.chat_id,
        username=user.username,
    )


def user_to_orm(user: UserDomain) -> UserOrm:
    return UserOrm(
        first_name=user.first_name,
        last_name=user.last_name,
        chat_id=user.chat_id,
        username=user.username,
    )
