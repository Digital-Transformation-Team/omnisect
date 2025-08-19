from collections.abc import Callable
from typing import Protocol

from pydantic import BaseModel

from utils import generate_get_config_method


class AppConfig(BaseModel):
    openai_api_key: str


def _get_config(get_value: Callable[[str], str], is_test: bool) -> dict:
    return dict(
        openai_api_key=get_value("OPENAI_API_KEY"),
    )


class GetAppConfigCallable(Protocol):
    def __call__(self, yaml_file: str = "app.yaml", **defaults) -> AppConfig: ...


get_app_config: GetAppConfigCallable = generate_get_config_method(
    AppConfig, _get_config
)
