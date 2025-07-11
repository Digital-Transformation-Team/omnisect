from dishka import Provider, Scope, provide

from plugins.core.iplugin import IPlugin
from plugins.helpers import LogUtil
from plugins.models import PluginServices
from plugins.plugin_use_case_service import PluginUseCase
from src.proxies.transcriber_proxy import TranscriberProxy
from src.services.plugin_service import PluginService


class PluginUseCaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_service(self) -> PluginUseCase:
        service = PluginUseCase()
        service.discover_plugins()
        return service

    @provide(scope=Scope.APP)
    def provide_registered_plugins(
        self, plugin_use_case: PluginUseCase, transcriber_proxy: TranscriberProxy
    ) -> list[IPlugin]:
        # TODO: Move it to lifespan module
        logger = LogUtil.create()
        plugins = [
            plugin_use_case.register_plugin(
                mdl,
                logger,
                plugin_deps=PluginServices(transcriber_proxy=transcriber_proxy),
            )
            for mdl in plugin_use_case.modules
        ]
        return plugins


class ServiceProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def get_plugin_service(
        self, plugin_use_case: PluginUseCase, registered_plugins: list[IPlugin]
    ) -> PluginService:
        return PluginService(
            plugin_use_case_service=plugin_use_case,
            registered_plugins=registered_plugins,
        )

    @provide(scope=Scope.APP)
    def get_transcriber_proxy(self) -> TranscriberProxy:
        return TranscriberProxy()
