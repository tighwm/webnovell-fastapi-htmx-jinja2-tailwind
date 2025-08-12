from typing import Annotated

from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from rest.services import auth as auth_serv
from rest.schemas.user import RegistrationForm
from utils.templates import templates
from core.models import db_helper

router = APIRouter(prefix="/auth")

COOKIE_SESSION_ID = "_session_id"


@router.get("/login", name="auth-login")
async def index_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
    )


@router.post("/login", name="auth-login-post")
async def handle_login(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    user_session = await auth_serv.login(
        username=username,
        password=password,
        session=session,
    )
    if user_session is None:
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={"err": "Invalid login or password."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    response = RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.set_cookie(
        key=COOKIE_SESSION_ID,
        value=str(user_session.jti),
        httponly=True,
    )
    return response


@router.get("/register", name="auth-register")
async def index_register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/register.html",
    )


@router.post("/register", name="auth-register-post")
async def handle_register(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    form = await request.form()
    form = RegistrationForm.validate_form(form)
    if form.errors:
        return templates.TemplateResponse(
            request=request,
            name="auth/register.html",
            context={"form": form},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    user_session = await auth_serv.register(
        user_in=form,
        session=session,
    )
    response = RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.set_cookie(
        key=COOKIE_SESSION_ID,
        value=str(user_session.jti),
        httponly=True,
    )
    return response
