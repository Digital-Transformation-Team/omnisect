from dishka import make_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from di.providers import PluginUseCaseProvider, ServiceProvider
from web.routers import plugins_router


def create_web_application():
    app = FastAPI()
    app.include_router(plugins_router.router)
    container = make_container(ServiceProvider(), PluginUseCaseProvider())
    setup_dishka(container=container, app=app)
    return app


app = create_web_application()
