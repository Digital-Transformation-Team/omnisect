from dishka import Provider, Scope, provide_all

from src.services.plugin_service import PluginService


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    # Services
    services = provide_all(PluginService)
