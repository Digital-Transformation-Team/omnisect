from abc import ABC, abstractmethod
from logging import Logger
from typing import Optional

from plugins.models import Meta
from plugins.core.iplugin_registry import IPluginRegistry


class IPlugin(ABC, metaclass=IPluginRegistry):

    meta = Optional[Meta]

    def __init__(self, logger: Logger):
        """
        Entry init block for plugins
        :param logger: logger that plugins can make use of
        """
        self.logger = logger

    @abstractmethod
    def invoke(self, **args) -> str:
        """
        Starts main plugin flow
        :param args: possible arguments for the plugin
        :return: something?
        """
        raise NotImplementedError()
