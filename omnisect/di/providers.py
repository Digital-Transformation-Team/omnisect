from dishka import Provider, Scope, provide
from plugins.plugin_use_case_service import PluginUseCase
from src.services.plugin_service import PluginService


class PluginUseCaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_service(self) -> PluginUseCase:
        service = PluginUseCase()
        service.discover_plugins()
        return service


class ServiceProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def get_plugin_service(self, plugin_use_case: PluginUseCase) -> PluginService:
        return PluginService(plugin_use_case_service=plugin_use_case)
