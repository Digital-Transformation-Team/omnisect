import logging
import os
import sys
from logging import DEBUG, Logger, StreamHandler

import yaml

from fs_config import get_fs_config


class FileSystem:
    @staticmethod
    def get_base_dir():
        """At most all application packages are just one level deep"""
        current_path = os.path.abspath(os.path.dirname(__file__))
        return current_path

    @staticmethod
    def get_plugins_directory() -> str:
        cfg = get_fs_config()
        return cfg.plugins_folder_path

    @staticmethod
    def get_outputs_directory() -> str:
        cfg = get_fs_config()
        return cfg.outputs_folder_path

    @staticmethod
    def load_configuration(name, config_directory) -> dict:
        with open(os.path.join(config_directory, name)) as file:
            input_data = yaml.safe_load(file)
        return input_data


class LogUtil(Logger):
    __FORMATTER = (
        "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s"
    )

    def __init__(
        self,
        name: str,
        log_format: str = __FORMATTER,
        level: int | str = DEBUG,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(name, level)
        self.formatter = logging.Formatter(log_format)
        self.addHandler(self.__get_stream_handler())

    def __get_stream_handler(self) -> StreamHandler:
        handler = StreamHandler(sys.stdout)
        handler.setFormatter(self.formatter)
        return handler

    @staticmethod
    def create(log_level: str = "DEBUG") -> Logger:
        logging.setLoggerClass(LogUtil)
        logger = logging.getLogger("plugin.architecture")
        logger.setLevel(log_level)
        return logger
