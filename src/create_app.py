from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from core.models import db_helper

# from utils import minio_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await minio_helper.create_buckets_if_not_exists(["novel-cover"])
    yield
    await db_helper.dispose()


def create_app():
    app = FastAPI(
        default_response_class=HTMLResponse,
        lifespan=lifespan,
    )
    app.mount(
        "/static",
        StaticFiles(directory="static"),
        name="static",
    )
    return app
