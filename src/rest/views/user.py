from typing import Annotated

from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from rest.cruds import user as user_crud
from utils.templates import templates

router = APIRouter(prefix="/user")


@router.get("/{user_id}", name="user-profile")
async def get_user_profile(
    request: Request,
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    user = await user_crud.get_by_id(
        session=session,
        user_id=user_id,
    )
    if user is None:
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return templates.TemplateResponse(
        request=request,
        name="user/profile.html",
        context={"user": user},
    )
