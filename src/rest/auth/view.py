from typing import Annotated

from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse

from rest.auth.service import validate_form
from utils.templates import templates

router = APIRouter(prefix="/auth")


@router.get("/login", name="auth-login")
async def index_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
    )


@router.post("/login", name="auth-login-post")
async def handle_login(request: Request):
    pass


@router.get("/register", name="auth-register")
async def index_register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/register.html",
    )


@router.post("/register", name="auth-register-post")
async def handle_register(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    ctx = {"username": username, "password": password}
    if not validate_form(ctx):
        return templates.TemplateResponse(
            request=request,
            name="auth/register.html",
            context=ctx,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
