from typing import Annotated

from fastapi import APIRouter, Request, Depends

from core.models import User
from rest.services.auth import get_user_by_user_session
from rest.views.auth import router as auth_router, COOKIE_SESSION_ID
from rest.cruds import session as session_crud
from utils.templates import templates

router = APIRouter()


@router.get("/", name="home")
async def index_page(
    request: Request,
    user: Annotated[User | None, Depends(get_user_by_user_session)],
):
    if user is None:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
        )
    return templates.TemplateResponse(
        request=request,
        name="index-for-auth.html",
        context={"user": user},
    )


router.include_router(auth_router)
