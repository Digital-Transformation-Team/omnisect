import datetime
import os

import pytest
from openai import OpenAI

from plugins.helpers import LogUtil
from plugins.models import PluginServices
from src.proxies.transcriber_proxy import TranscriberProxy
from src.utils import DatetimeUtils


class BaseTest:
    @pytest.fixture(scope="class", autouse=True)
    def set_python_env(self):
        os.environ["PYTHON_ENV"] = "test"

    @pytest.fixture
    def logger(self):
        return LogUtil.create()

    @pytest.fixture(autouse=True)
    def patch_datetime_utils_now_iso_str(self, monkeypatch):
        def _now_iso_str(*args, **kwargs):
            return datetime.datetime(2024, 1, 1, 12, 0).isoformat(
                timespec="milliseconds"
            )

        monkeypatch.setattr(DatetimeUtils, "now_iso_str", _now_iso_str)

    @pytest.fixture
    def plugin_services(self):
        return PluginServices(
            transcriber_proxy=TranscriberProxy(),
            openai_client=OpenAI(api_key="wrong-key"),
        )
