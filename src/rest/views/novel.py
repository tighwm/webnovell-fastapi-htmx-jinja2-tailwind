from typing import Annotated

from fastapi import APIRouter, Request, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from utils.templates import templates
from rest.cruds import novel as novel_crud

router = APIRouter(prefix="/novel")


@router.get("/new", name="create-novel-index")
async def handle_create_novel_index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="novel/novel-create.html",
    )


@router.get("/{novel_id}")
async def handle_novel_index(
    request: Request,
    novel_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    novel = await novel_crud.get_novel_by_id(
        session=session,
        novel_id=novel_id,
    )
    if novel is None:
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return templates.TemplateResponse(
        request=request,
        name="novel/novel.html",
        context={"novel": novel},
    )
