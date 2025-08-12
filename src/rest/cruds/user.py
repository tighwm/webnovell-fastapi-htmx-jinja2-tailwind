from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.models import User
from rest.schemas.user import RegistrationForm


async def create(
    session: AsyncSession,
    user_in: RegistrationForm,
) -> User | None:
    user_orm = User(**user_in.model_dump(exclude_none=True))
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


async def get_by_id(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    return await session.get(User, user_id)
