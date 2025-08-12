from typing import Annotated

from fastapi import APIRouter, Request, Depends, status
from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from utils import templates, minio_helper
from rest.cruds import novel as novel_crud
from rest.services import novel as novel_serv
from rest.schemas.novel import NovelForm

router = APIRouter(prefix="/novel")


@router.get("/new", name="create-novel-index")
async def handle_create_novel_index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="novel/create.html",
    )


@router.post("/new", name="create-novel")
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


@router.get("/{novel_id}", name="novel-page")
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
