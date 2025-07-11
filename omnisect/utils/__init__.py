import os
from collections.abc import Callable
from os import environ
from pathlib import Path
from threading import RLock

from .lock import with_lock
from .read_config_file import read_config_file

_config_lock = RLock()
_config_cache: dict[type, object] = {}


@with_lock(lock=_config_lock)
def clear_config_cache(type: type | None = None):
    global _config_cache

    if type is None:
        _config_cache.clear()
    elif type in _config_cache:
        del _config_cache[type]


def generate_get_config_method(
    t: type, get_config: Callable[[Callable[[str], str], bool], dict]
):
    @with_lock(lock=_config_lock)
    def _method(file: str = "app.yaml", **defaults) -> type:
        if t in _config_cache:
            return _config_cache[t]

        yaml = read_config_file(file)

        def _get_value(key: str):
            for src in [environ, yaml, defaults]:
                value = src.get(key)
                if value is not None:
                    return value

        is_test = _get_value("PYTHON_ENV") == "test"
        config = get_config(_get_value, is_test)
        _config_cache[t] = t(**config)
        return _config_cache[t]

    return _method


def _find_project_dir() -> str | None:
    cwd = Path(os.getcwd())
    while not os.path.exists(os.path.join(str(cwd), "app.yaml")):
        cwd = Path(cwd.parent)
        if cwd == Path("/"):
            return

    return str(cwd)


def replace_known_dirs(p: str | None):
    if p is None:
        return

    project_dir = _find_project_dir()
    if project_dir is None:
        project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    return p.replace("$HOME", str(Path.home())).replace("$PROJECT", project_dir)


def has_keys(d: dict, keys: list) -> bool:
    for key in keys:
        if key not in d or not d[key]:
            return False
    return True
