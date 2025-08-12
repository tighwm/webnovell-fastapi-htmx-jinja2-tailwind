import uuid

from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from rest.schemas.novel import NovelForm, NovelToDB
from rest.cruds import novel as novel_crud


async def create_novel(
    session: AsyncSession,
    minio: Minio,
    novel_in: NovelForm,
):
    obj_cover_name = uuid.uuid4()
    obj_cover = await minio.put_object(
        bucket_name="novel-cover",
        object_name=str(obj_cover_name),
        data=novel_in.img.file,
        length=novel_in.img.size,
        content_type=novel_in.img.content_type,
    )
    novel_to_db = NovelToDB(**novel_in.model_dump(), obj_cover_name=obj_cover_name)
    novel = await novel_crud.create(
        session=session,
        novel_in=novel_to_db,
    )
    return novel
