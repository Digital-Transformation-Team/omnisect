from logging import Logger
from plugins.core.iplugin import IPlugin
from plugins.plugin_use_case_service import PluginUseCase
from src.dto import plugin_dto
from src.errors.types import NotFoundError


class PluginService:
    def __init__(self, plugin_use_case_service: PluginUseCase):
        self._logger = Logger(name=__name__)
        self._plugin_use_case_service = plugin_use_case_service

    def _get_plugin_by_web_id(self, web_id: str) -> IPlugin | None:
        plugin = next(
            (
                plugin
                for plugin in self._plugin_use_case_service.plugins
                if plugin.meta.web_id == web_id
            ),
            None,
        )
        if not plugin:
            raise NotFoundError("_error_plugin_not_found:", web_id)
        return plugin

    def list_plugins(self) -> list[plugin_dto.Read]:
        return [
            plugin_dto.Read.from_model(plugin)
            for plugin in self._plugin_use_case_service.plugins
        ]

    def get_plugin(self, web_id: str) -> plugin_dto.Read:
        return plugin_dto.Read.from_model(self._get_plugin_by_web_id(web_id=web_id))

    def invoke_plugin(self, web_id: str) -> str:
        plugin = self._get_plugin_by_web_id(web_id=web_id)
        return self._plugin_use_case_service.hook_plugin(plugin, "some text")
