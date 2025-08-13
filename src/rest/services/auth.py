import uuid
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from core.models import UserSession, db_helper
from core.security.passwords import hash_password, validate_password
from rest.cruds import user as user_crud, session as session_crud
from rest.schemas.user import RegistrationForm

COOKIE_SESSION_ID = "_session_id"


async def login(
    username: str,
    password: str,
    session: AsyncSession,
) -> UserSession | None:
    user = await user_crud.get_by_username(
        session=session,
        username=username,
    )
    if user is None:
        return None
    if not validate_password(password, user.hashed_password):  # type: ignore
        return None

    jti = uuid.uuid4()
    user_session = await session_crud.create(session=session, jti=jti, user_id=user.id)  # type: ignore
    return user_session


async def register(
    user_in: RegistrationForm,
    session: AsyncSession,
) -> UserSession:
    user_in.password = hash_password(user_in.password)
    user = await user_crud.create(
        user_in=user_in,
        session=session,
    )
    jti = uuid.uuid4()
    return await session_crud.create(session, jti, user.id)  # type: ignore


async def get_user_by_user_session(
    request: Request,
    session: AsyncSession,
):
    session_id: str | None = request.cookies.get(COOKIE_SESSION_ID)
    if not session_id:
        return None
    user_session = await session_crud.get_by_jti(
        session=session,
        jti=uuid.UUID(session_id),
        with_user=True,
    )
    if not user_session:
        return None
    return user_session.user
