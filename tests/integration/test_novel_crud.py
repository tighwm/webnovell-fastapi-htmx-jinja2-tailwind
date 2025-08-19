from tests.conftest import test_session


async def test_create_novel(test_session):
    from rest.cruds.novel import create
    from rest.schemas.novel import NovelToDB
    from core.models import Novel

    novel_in = NovelToDB(
        title="Shadow Slave",
        obj_cover_name=None,
    )

    result = await create(test_session, novel_in)

    assert result is not None
    assert isinstance(result, Novel)
    fetched = await test_session.get(Novel, result.id)
    assert fetched is not None
    assert fetched.title == result.title
    assert fetched.id == result.id


async def test_get_by_id_novel(test_session):
    from tests.factories import NovelFactory
    from rest.cruds.novel import get_novel_by_id
    from core.models import Novel

    novel = await NovelFactory()

    result = await get_novel_by_id(
        session=test_session,
        novel_id=novel.id,
    )

    assert result is not None
    assert isinstance(result, Novel)
    assert novel.id == result.id
    assert novel.title == result.title
    assert novel.obj_cover_name == result.obj_cover_name
