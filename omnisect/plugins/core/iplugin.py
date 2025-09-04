import hashlib
from abc import ABC, abstractmethod
from logging import Logger

from plugins.core.iplugin_registry import IPluginRegistry
from plugins.models import Meta, PluginConfig, PluginInput, PluginOutput, PluginServices


class IPlugin(ABC, metaclass=IPluginRegistry):
    meta = Meta | None

    def __init__(
        self,
        logger: Logger,
        plugin_services: PluginServices,
        plugin_config: PluginConfig,
    ):
        """
        Entry init block for plugins
        :param logger: logger that plugins can make use of
        """
        self.logger = logger
        self.meta = Meta(
            name=plugin_config.name,
            description=plugin_config.description,
            version=plugin_config.version,
            creator=plugin_config.creator,
            instructions=plugin_config.instructions.to_text(
                plugin_name=plugin_config.name
            )
            if plugin_config.instructions is not None
            else None,
            web_id=self._generate_web_id(config=plugin_config),
        )
        self._plugin_services = plugin_services

    @abstractmethod
    def invoke(self, input: PluginInput) -> PluginOutput:
        """
        Starts main plugin flow
        :param args: possible arguments for the plugin
        :return: PluginOutput
        """
        raise NotImplementedError()

    def _generate_web_id(self, config: PluginConfig) -> str:
        base = f"{config.name}:{config.alias}:{config.creator}"
        return hashlib.md5(base.encode("utf-8")).hexdigest()
