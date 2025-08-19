from collections.abc import Iterable

from dishka import Provider

from ioc.providers import PluginUseCaseProvider, ServiceProvider


def get_providers() -> Iterable[Provider]:
    return (ServiceProvider(), PluginUseCaseProvider())
