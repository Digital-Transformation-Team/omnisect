from abc import ABC, abstractmethod
from logging import Logger
from typing import Optional

from plugins.models import Meta, PluginServices, PluginInput, PluginOutput
from plugins.core.iplugin_registry import IPluginRegistry


class IPlugin(ABC, metaclass=IPluginRegistry):

    meta = Optional[Meta]

    def __init__(self, logger: Logger, plugin_services: PluginServices):
        """
        Entry init block for plugins
        :param logger: logger that plugins can make use of
        """
        self.logger = logger
        self._plugin_services = plugin_services

    @abstractmethod
    def invoke(self, input: PluginInput) -> PluginOutput:
        """
        Starts main plugin flow
        :param args: possible arguments for the plugin
        :return: PluginOutput
        """
        raise NotImplementedError()
