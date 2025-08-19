from factory import Sequence, alchemy, Faker

from core.models import Novel
from tests import database
from tests.factory_ import AsyncSQLAlchemyModelFactory


class BaseFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_factory = database.async_scoped_session
        sqlalchemy_session_persistence = alchemy.SESSION_PERSISTENCE_FLUSH


class NovelFactory(BaseFactory):
    class Meta:
        model = Novel

    id = Sequence(lambda i: i + 1)
    title = Faker("name")
    obj_cover_name = None
