from typing import Optional
from sqlalchemy import select, exists
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User, UserProfile


async def test_connection(session: AsyncSession) -> Optional[int]:
    """
    Проверка соединения с СУБД
    :param session: объект AsyncSession
    """
    try:
        stmt = select(1)
        return await session.scalar(stmt)
    except Exception as e:

        return None


async def get_user_by_telegram_id(
    session: AsyncSession,
    telegram_id: int,
) -> User | None:
    """Проверка существания User"""
    try:
        stmt = select(User).where(User.telegram_id == telegram_id)
        user = await session.scalar(stmt)

        if user is not None:
            return user

    except Exception as e:
        print(str(e))


async def checking_profile_existence(
    session: AsyncSession,
    telegram_id: int,
) -> bool:
    """Проверка существания профиля анкеты пользователя"""
    try:
        user = await get_user_by_telegram_id(session, telegram_id)

        stmt = select(exists().where(UserProfile.user_id == user.id))
        result = await session.scalar(stmt)

        return result or False

    except Exception as e:
        print(str(e))


async def get_userprofile(
    session: AsyncSession,
    telegram_id: int,
) -> UserProfile | bool:
    try:
        await checking_profile_existence(session, telegram_id)

    except Exception as e:
        return False


async def update_ml_answer_userprofile(
    session: AsyncSession,
    answer: float,
    telegram_id: int,
):

    # user_profile = await checking_user_existence(session, telegram_id)
    # if user:
    #     user.user_profile.ml_answer = answer
    pass
