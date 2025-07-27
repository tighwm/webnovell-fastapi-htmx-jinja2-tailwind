from fastapi import APIRouter, Request

from rest.auth.view import router as auth_router
from utils.templates import templates

router = APIRouter()


@router.get("/", name="home")
def index_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


router.include_router(auth_router)
