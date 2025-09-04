from dishka import Provider, Scope
from openai import OpenAI

from app_config import AppConfig
from plugins.core.iplugin import IPlugin
from plugins.helpers import LogUtil
from plugins.models import PluginServices
from plugins.plugin_use_case_service import PluginUseCase
from src.proxies.transcriber_proxy import TranscriberProxy


def get_plugin_use_case() -> PluginUseCase:
    service = PluginUseCase()
    service.discover_plugins()
    return service


def get_transcriber_proxy() -> TranscriberProxy:
    return TranscriberProxy()


def get_plugins(
    plugin_use_case: PluginUseCase,
    transcriber_proxy: TranscriberProxy,
    openai_client: OpenAI,
) -> list[IPlugin]:
    logger = LogUtil.create()
    plugins = [
        plugin_use_case.register_plugin(
            mdl,
            logger,
            plugin_deps=PluginServices(
                transcriber_proxy=transcriber_proxy, openai_client=openai_client
            ),
            plugin_config=config,
        )
        for mdl, config in plugin_use_case.modules.items()
    ]
    return plugins


def get_openai_client(config: AppConfig) -> OpenAI:
    return OpenAI(api_key=config.openai_api_key)


class InfrastructureProvider(Provider):
    scope = Scope.REQUEST


def infrastructure_provider():
    provider = InfrastructureProvider()
    provider.provide(
        source=get_transcriber_proxy,
        scope=Scope.APP,
    )
    provider.provide(
        source=get_plugin_use_case,
        scope=Scope.APP,
    )
    provider.provide(
        source=get_plugins,
        scope=Scope.APP,
    )
    provider.provide(
        source=get_openai_client,
        scope=Scope.APP,
    )
    return provider
