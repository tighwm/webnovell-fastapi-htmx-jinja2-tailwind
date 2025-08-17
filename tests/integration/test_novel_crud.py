from tests.conftest import test_session


async def test_create_novel(test_session):
    from rest.cruds import novel as novel_crud
    from rest.schemas.novel import NovelToDB
    from core.models import Novel

    novel_in = NovelToDB(
        title="Shadow Slave",
        obj_cover_name=None,
    )

    result = await novel_crud.create(test_session, novel_in)

    assert result is not None
    assert isinstance(result, Novel)
    fetched = await test_session.get(Novel, result.id)
    assert fetched is not None
    assert fetched.title == result.title
    assert fetched.id == result.id
