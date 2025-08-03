from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.models import User


async def create(
    session: AsyncSession,
    user_in: dict[str, str],
) -> User | None:
    user_orm = User(**user_in)
    session.add(user_orm)
    try:
        await session.flush()
    except IntegrityError:
        await session.rollback()
        return None
    await session.refresh(user_orm)
    return user_orm


async def get_by_username(
    session: AsyncSession,
    username: str,
) -> User | None:
    stmt = select(User).where(User.username == username)
    user = await session.scalar(stmt)
    return user
