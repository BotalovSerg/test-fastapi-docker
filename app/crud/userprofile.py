from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


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
