from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Novel


async def get_novel_by_id(
    session: AsyncSession,
    novel_id: int,
) -> Novel | None:
    return await session.get(Novel, novel_id)
