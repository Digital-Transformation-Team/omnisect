from abc import ABCMeta


class IPluginRegistry(ABCMeta):
    plugins = []

    def __init__(cls, name, bases, attrs):
        super().__init__(cls)
        if not cls.__abstractmethods__:
            IPluginRegistry.plugins.append(cls)
