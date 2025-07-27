import uvicorn

from create_app import create_app
from rest import router as rest_router
from core.config import settings

main_app = create_app()

main_app.include_router(rest_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
    )
