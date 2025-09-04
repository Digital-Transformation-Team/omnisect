import os

import pytest


class BaseTest:
    @pytest.fixture(scope="class", autouse=True)
    def set_python_env(self):
        os.environ["PYTHON_ENV"] = "test"
