from collections.abc import Callable
from typing import Protocol

from pydantic import BaseModel

from utils import generate_get_config_method


class AppConfig(BaseModel):
    # LLM configuration
    openai_api_key: str
    llm_model: str
    llm_temperature: float
    llm_max_tokens: int


def _get_config(get_value: Callable[[str], str], is_test: bool) -> dict:
    return dict(
        openai_api_key=get_value("OPENAI_API_KEY"),
        llm_model=get_value("LLM_MODEL"),
        llm_temperature=get_value("LLM_TEMPERATURE"),
        llm_max_tokens=get_value("LLM_MAX_TOKENS"),
    )


class GetAppConfigCallable(Protocol):
    def __call__(self, yaml_file: str = "app.yaml", **defaults) -> AppConfig: ...


get_app_config: GetAppConfigCallable = generate_get_config_method(
    AppConfig, _get_config
)
