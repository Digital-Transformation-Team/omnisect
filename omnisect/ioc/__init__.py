from collections.abc import Iterable

from dishka import Provider, make_async_container

from app_config import AppConfig


def create_async_ioc_container(providers: Iterable[Provider], config: AppConfig):
    return make_async_container(*providers, context={AppConfig: config})
