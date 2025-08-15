import logging
from typing import Annotated

from fastapi import APIRouter, Request, Depends, status
from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from utils import templates, minio_helper
from rest.services import novel as novel_serv, auth as auth_serv
from rest.cruds import novel as novel_crud
from rest.schemas.novel import NovelForm
from utils.loggers import log_handler

router = APIRouter(prefix="/novel")

log = logging.getLogger(__name__)


@router.get("/new", name="create-novel-index")
@log_handler(log)
async def handle_create_novel_index(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    response_404 = templates.TemplateResponse(
        request=request,
        name="404.html",
        status_code=status.HTTP_404_NOT_FOUND,
    )
    user = await auth_serv.get_user_by_user_session(request, session)
    if user is None:
        return response_404
    return templates.TemplateResponse(
        request=request,
        name="novel/create.html",
        context={"user": user},
    )


@router.post("/new", name="create-novel")
@log_handler(log)
async def handle_create_novel(
    request: Request,
    minio: Annotated[Minio, Depends(minio_helper.minio_getter)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    form = await request.form()
    form = NovelForm.validate_form(form)
    if form.errors:
        return templates.TemplateResponse(
            request=request,
            name="novel/components/creating-form-err.html",
            context={"form": form},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    novel = await novel_serv.create_novel(
        session=session,
        minio=minio,
        novel_in=form,
    )
    return templates.TemplateResponse(
        request=request,
        name="novel/components/create-success.html",
        context={"novel": novel},
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/search", name="novel-search")
@log_handler(log)
async def handle_search(
    request: Request,
    q: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    res = await novel_crud.search_novels_by_title(
        session=session,
        title=q,
    )
    return templates.TemplateResponse(
        request=request,
        name="novel/components/search-result.html",
        context={"res": res},
    )


@router.get("/{novel_id}", name="novel-page")
@log_handler(log)
async def handle_novel_index(
    request: Request,
    novel_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    minio: Annotated[Minio, Depends(minio_helper.minio_getter)],
):
    response_404 = templates.TemplateResponse(
        request=request,
        name="404.html",
        status_code=status.HTTP_404_NOT_FOUND,
    )
    user = await auth_serv.get_user_by_user_session(request, session)
    if user is None:
        return response_404
    novel = await novel_serv.get_novel(
        session=session,
        minio=minio,
        novel_id=novel_id,
    )
    if novel is None:
        return response_404
    return templates.TemplateResponse(
        request=request,
        name="novel/novel.html",
        context={
            "novel": novel,
            "user": user,
        },
    )
