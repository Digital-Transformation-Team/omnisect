from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles

from app_config import get_app_config
from ioc import create_async_ioc_container
from ioc.provider_registry import get_providers
from src.errors.types import (
    ForbiddenError,
    InvalidContentTypeError,
    InvalidCredentialsError,
    InvalidDataError,
    InvalidTokenError,
    NotFoundError,
    ValidationError,
)
from web.errors.handler import generate_default_error_handler
from web.routers import plugins_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield None
    await app.state.dishka_container.close()
    # https://dishka.readthedocs.io/en/stable/integrations/fastapi.html


def create_web_application(
    errors_mapping: dict[type[Exception], int] | None = None,
):
    app = FastAPI(lifespan=lifespan)
    em: dict[type[Exception], int] = {
        ValidationError: status.HTTP_400_BAD_REQUEST,
        InvalidDataError: status.HTTP_400_BAD_REQUEST,
        InvalidTokenError: status.HTTP_401_UNAUTHORIZED,
        InvalidCredentialsError: status.HTTP_401_UNAUTHORIZED,
        InvalidContentTypeError: status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        NotFoundError: status.HTTP_404_NOT_FOUND,
        ForbiddenError: status.HTTP_403_FORBIDDEN,
    }
    em.update(errors_mapping or dict())
    app.add_exception_handler(Exception, generate_default_error_handler(em))
    app.mount("/outputs", StaticFiles(directory="plugins/outputs"), name="outputs")
    app.include_router(plugins_router.router)
    config = get_app_config()

    # di
    config = get_app_config()
    async_ioc_container = create_async_ioc_container(
        providers=get_providers(),
        config=config,
    )
    setup_dishka(container=async_ioc_container, app=app)
    return app


app = create_web_application()
