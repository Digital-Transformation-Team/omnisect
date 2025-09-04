import os
from functools import cached_property
from importlib import import_module
from logging import Logger
from typing import Any

from fs_config import get_fs_config
from plugins.core import IPlugin, IPluginRegistry
from plugins.helpers import LogUtil
from plugins.models import PluginConfig, PluginInput, PluginServices
from plugins.utils import PluginUtility


class PluginUseCase:
    _logger: Logger
    modules: list[type]

    def __init__(self) -> None:
        self._logger = LogUtil.create()
        self.plugin_util = PluginUtility(self._logger)
        # {SamplePlugin: PluginConfig()}
        self.modules = dict()

    @cached_property
    def plugins(self) -> list[IPlugin]:
        return [
            self.register_plugin(module, logger=self._logger, plugin_config=config)
            for module, config in self.modules
        ]

    def __check_loaded_plugin_state(self, plugin_module: Any, plugin_config):
        if len(IPluginRegistry.plugins) > 0:
            latest_module = IPluginRegistry.plugins[-1]
            latest_module_name = latest_module.__module__
            current_module_name = plugin_module.__name__
            if current_module_name == latest_module_name:
                self._logger.debug(
                    f"Successfully imported module `{current_module_name}`"
                )
                self.modules[latest_module] = plugin_config
            else:
                self._logger.error(
                    f"Expected to import -> `{current_module_name}` but got -> `{latest_module_name}`"
                )
            # clear plugins from the registry when we're done with them
            IPluginRegistry.plugins.clear()
        else:
            self._logger.error(
                f"No plugin found in registry for module: {plugin_module}"
            )

    def __search_for_plugins_in(self, plugins_path: list[str], package_name: str):
        for directory in plugins_path:
            entry_point, plugin_config = self.plugin_util.setup_plugin_configuration(
                package_name, directory
            )
            if entry_point is not None:
                plugin_entry, _ = os.path.splitext(entry_point)
                # Importing the module will cause IPluginRegistry to invoke it's __init__ fun
                cfg = get_fs_config()
                import_target_module = (
                    f"{cfg.plugins_namespace_prefix}.{directory}.{plugin_entry}"
                )
                module = import_module(import_target_module, package_name)
                self.__check_loaded_plugin_state(module, plugin_config)
            else:
                self._logger.debug(f"No valid plugin found in {package_name}")

    def discover_plugins(self, reload: bool = True):
        """
        Discover the plugin classes contained in Python files, given a
        list of directory names to scan.
        """
        fs_config = get_fs_config()
        if reload:
            self.modules.clear()
            IPluginRegistry.plugins.clear()
            self._logger.debug(
                f"Searching for plugins under package {fs_config.plugins_folder_path}"
            )
            plugins_path = PluginUtility.filter_plugins_paths(
                fs_config.plugins_folder_path
            )
            package_name = os.path.basename(
                os.path.normpath(fs_config.plugins_folder_path)
            )
            self.__search_for_plugins_in(plugins_path, package_name)

    @staticmethod
    def register_plugin(
        module: type,
        logger: Logger,
        plugin_deps: PluginServices,
        plugin_config: PluginConfig,
    ) -> IPlugin:
        """
        Create a plugin instance from the given module
        :param module: module to initialize
        :param logger: logger for the module to use
        :return: a high level plugin
        """
        return module(logger, plugin_deps, plugin_config)

    @staticmethod
    def hook_plugin(plugin: IPlugin, input: PluginInput):
        """
        Return a function accepting commands.
        """
        return plugin.invoke(input)
