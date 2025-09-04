from collections.abc import Iterable

from dishka import Provider

from ioc.application_provider import ApplicationProvider
from ioc.infrastructure_provider import infrastructure_provider


def get_providers() -> Iterable[Provider]:
    return (ApplicationProvider(), infrastructure_provider())
