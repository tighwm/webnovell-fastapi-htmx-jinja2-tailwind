from fastapi import APIRouter, Request

from utils.templates import templates

router = APIRouter(prefix="/auth")


@router.get("/login", name="auth-index")
async def index_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/index.html",
    )
