from typing import Any

from factory import alchemy, enums
from factory.alchemy import SQLAlchemyOptions
from factory.base import Factory, FactoryMetaClass, StubObject, T
from factory.errors import UnknownStrategy
from sqlalchemy.util import await_only, greenlet_spawn


class AsyncFactoryMetaClass(FactoryMetaClass):  # type: ignore[misc]
    async def __call__(cls, **kwargs: Any) -> T | StubObject:  # noqa: ANN401,N805
        if cls._meta.strategy == enums.BUILD_STRATEGY:
            return cls.build(**kwargs)

        if cls._meta.strategy == enums.CREATE_STRATEGY:
            return await cls.create(**kwargs)

        if cls._meta.strategy == enums.STUB_STRATEGY:
            return cls.stub(**kwargs)

        raise UnknownStrategy(
            f"Unknown '{cls.__name__}.Meta.strategy': {cls._meta.strategy}"
        )


class AsyncSQLAlchemyModelFactory(Factory, metaclass=AsyncFactoryMetaClass):  # type: ignore[misc]
    _options_class = SQLAlchemyOptions

    class Meta:
        abstract = True

    @classmethod
    async def create(cls, **kwargs: Any) -> T:  # noqa: ANN401
        return await greenlet_spawn(cls._generate, enums.CREATE_STRATEGY, kwargs)

    @classmethod
    async def create_batch(cls, size: int, **kwargs: Any) -> list[T]:  # noqa: ANN401
        return [await cls.create(**kwargs) for _ in range(size)]

    @classmethod
    def _create(
        cls, model_class: type[Any], *args: Any, **kwargs: Any
    ) -> T:  # noqa: ANN401
        meta = cls._meta

        session = meta.sqlalchemy_session
        if (
            session is None
            and (session_factory := meta.sqlalchemy_session_factory) is not None
        ):
            session = session_factory()

        if not session:
            class_name = cls.__name__
            raise RuntimeError(
                f"No session: "
                f"set '{class_name}.Meta.sqlalchemy_session' or '{class_name}.Meta.sqlalchemy_session_factory'"
            )

        instance = model_class(*args, **kwargs)
        session.add(instance)

        session_persistence = meta.sqlalchemy_session_persistence
        if session_persistence == alchemy.SESSION_PERSISTENCE_FLUSH:
            await_only(session.flush())
        elif session_persistence == alchemy.SESSION_PERSISTENCE_COMMIT:
            await_only(session.commit())

        return instance
