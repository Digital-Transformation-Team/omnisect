from collections.abc import Callable
from typing import Protocol

from pydantic import BaseModel

from utils import generate_get_config_method, replace_known_dirs


class FsConfig(BaseModel):
    test_data_path: str
    file_storage_path: str
    plugins_folder_path: str
    outputs_folder_path: str
    plugins_namespace_prefix: str


def _get_config(get_value: Callable[[str], str], is_test: bool) -> dict:
    test_data_path = replace_known_dirs(get_value("TEST_DATA_PATH"))
    file_storage_path = replace_known_dirs(
        get_value("FILE_STORAGE_PATH_TEST" if is_test else "FILE_STORAGE_PATH")
    )
    plugins_folder_path = replace_known_dirs(
        get_value("PLUGINS_FOLDER_PATH_TEST" if is_test else "PLUGINS_FOLDER_PATH")
    )
    outputs_folder_path = replace_known_dirs(
        get_value("FILE_STORAGE_PATH_TEST" if is_test else "OUTPUTS_FOLDER_PATH")
    )
    plugins_namespace_prefix = replace_known_dirs(
        get_value(
            "PLUGINS_NAMESPACE_PREFIX_TEST" if is_test else "PLUGINS_NAMESPACE_PREFIX"
        )
    )
    return dict(
        test_data_path=test_data_path,
        file_storage_path=file_storage_path,
        plugins_folder_path=plugins_folder_path,
        outputs_folder_path=outputs_folder_path,
        plugins_namespace_prefix=plugins_namespace_prefix,
    )


class GetAppConfigCallable(Protocol):
    def __call__(self, yaml_file: str = "app.yaml", **defaults) -> FsConfig: ...


get_fs_config: GetAppConfigCallable = generate_get_config_method(FsConfig, _get_config)
