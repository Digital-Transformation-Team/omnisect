from dataclasses import dataclass
from typing import List, Optional

from src.proxies.transcriber_proxy import TranscriberProxy


@dataclass
class PluginRunTimeOption(object):
    main: str
    tests: Optional[List[str]]


@dataclass
class DependencyModule:
    name: str
    version: str

    def __str__(self) -> str:
        return f"{self.name}=={self.version}"


@dataclass
class PluginConfig:
    name: str
    alias: str
    creator: str
    runtime: PluginRunTimeOption
    repository: str
    description: str
    version: str
    requirements: Optional[List[DependencyModule]]


@dataclass
class Meta:
    web_id: str
    name: str
    description: str
    version: str

    def __str__(self) -> str:
        return f"{self.name}: {self.version}"


@dataclass
class PluginInput:
    text: str


@dataclass
class PluginOutput:
    text: str


@dataclass
class PluginServices:
    transcriber_proxy: TranscriberProxy
