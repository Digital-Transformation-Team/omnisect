from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app_config import get_app_config
from ioc import create_async_ioc_container
from ioc.registry import get_providers
from web.routers import plugins_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield None
    await app.state.dishka_container.close()


def create_web_application():
    app = FastAPI(lifespan=lifespan)
    app.include_router(plugins_router.router)
    config = get_app_config()
    container = create_async_ioc_container(providers=get_providers(), config=config)
    setup_dishka(container=container, app=app)
    return app


app = create_web_application()
