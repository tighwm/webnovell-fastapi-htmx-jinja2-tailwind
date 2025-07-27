from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


def create_app():
    app = FastAPI(
        default_response_class=HTMLResponse,
        lifespan=lifespan,
    )
    return app
