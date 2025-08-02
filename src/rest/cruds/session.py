import uuid

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import UserSession


async def create(
    session: AsyncSession,
    jti: uuid.UUID,
    user_id: int,
) -> UserSession:
    user_session = UserSession(jti=jti, user_id=user_id)
    session.add(user_session)
    await session.flush()
    return user_session


async def get_by_jti(
    session: AsyncSession,
    jti: uuid.UUID,
    with_user: bool = False,
) -> UserSession | None:
    stmt = select(UserSession).where(UserSession.jti == jti)
    if with_user:
        stmt = (
            select(UserSession)
            .options(
                joinedload(UserSession.user),
            )
            .where(UserSession.jti == jti)
        )
    user_session = await session.scalar(stmt)
    return user_session
