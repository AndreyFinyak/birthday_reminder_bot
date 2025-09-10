# import logging
# from functools import wraps

# from sqlalchemy.exc import IntegrityError, OperationalError
# from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# from app.config.settings import get_settings

# log = logging.getLogger(__name__)


# settings = get_settings()


# DATABASE_URL = settings.DATABASE_URL

# engine = create_async_engine(DATABASE_URL, echo=True)
# async_session_maker = async_sessionmaker(
#     engine, expire_on_commit=False, class_=AsyncSession
# )


# def connection(method):
#     """Декоратор для создания сессии базы данных"""

#     @wraps(method)
#     async def wrapper(*args, **kwargs):
#         async with async_session_maker() as session:
#             try:
#                 return await method(*args, session=session, **kwargs)
#             except IntegrityError as e:
#                 log.error("IntegrityError during DB operations: %s", e)
#                 await session.rollback()

#             except OperationalError as e:
#                 log.error("Database operational error: %s", e)
#                 await session.rollback()

#             except Exception as e:
#                 await session.rollback()
#                 raise e

#             finally:
#                 await session.close()

#     return wrapper
