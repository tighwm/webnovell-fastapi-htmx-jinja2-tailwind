from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import Novel
from rest.schemas.novel import NovelToDB


async def get_novel_by_id(
    session: AsyncSession,
    novel_id: int,
) -> Novel | None:
    return await session.get(Novel, novel_id)


async def create(
    session: AsyncSession,
    novel_in: NovelToDB,
):
    novel = Novel(**novel_in.model_dump())
    session.add(novel)
    await session.flush()
    return novel


async def search_novels_by_title(
    session: AsyncSession,
    title: str,
):
    stmt = select(Novel).where(Novel.title.bool_op("%")(title.lower()))
    result = await session.execute(stmt)
    return result.scalars().all()
