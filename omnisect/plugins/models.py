from dataclasses import dataclass

from openai import OpenAI
from pydantic import Field

from src.proxies.transcriber_proxy import TranscriberProxy


@dataclass
class PluginRunTimeOption:
    main: str
    tests: list[str] | None


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
    requirements: list[DependencyModule] | None


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
    language: str = Field(default="russian")


@dataclass
class PluginOutput:
    text: str


@dataclass
class PluginServices:
    transcriber_proxy: TranscriberProxy
    openai_client: OpenAI
