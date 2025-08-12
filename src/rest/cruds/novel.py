from sqlalchemy.ext.asyncio import AsyncSession

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
