# import uuid
# from datetime import timedelta

# from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Novel
from rest.schemas.novel import NovelForm, NovelToDB
from rest.cruds import novel as novel_crud


async def create_novel(
    session: AsyncSession,
    # minio: Minio,
    novel_in: NovelForm,
):
    obj_cover_name = None
    # if novel_in.img:
    #     obj_cover_name = uuid.uuid4()
    #     obj_cover = await minio.put_object(
    #         bucket_name="novel-cover",
    #         object_name=str(obj_cover_name),
    #         data=novel_in.img.file,
    #         length=novel_in.img.size,
    #         content_type=novel_in.img.content_type,
    #     )
    novel_to_db = NovelToDB(
        **novel_in.model_dump(),
        obj_cover_name=obj_cover_name,
    )
    novel = await novel_crud.create(
        session=session,
        novel_in=novel_to_db,
    )
    return novel


async def get_novel(
    session: AsyncSession,
    # minio: Minio,
    novel_id: int,
) -> Novel | None:
    novel = await novel_crud.get_novel_by_id(
        session=session,
        novel_id=novel_id,
    )
    if novel is None:
        return novel
    # if novel.obj_cover_name:
    #     cover_url = await minio.presigned_get_object(
    #         bucket_name="novel-cover",
    #         object_name=str(novel.obj_cover_name),  # type: ignore
    #         expires=timedelta(minutes=15),
    #     )
    #     novel.cover_url = cover_url
    return novel
