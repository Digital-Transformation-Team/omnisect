from logging import Logger
from unittest.mock import patch

from plugins.models import PluginConfig
from plugins.utils import PluginUtility
from tests.base_test import BaseTest


class TestPluginUtility(BaseTest):
    @patch("plugins.utils.subprocess.check_call")
    @patch("plugins.utils.distributions")
    def test_setup_plugin_configuration_should_load_sample_plugin(
        self, mock_distributions, mock_check_call
    ):
        mock_distributions.return_value = []
        mock_check_call.return_value = 0
        plugin_utility = PluginUtility(logger=Logger(name="test-logger", level="DEBUG"))

        assert (
            plugin_utility.setup_plugin_configuration(
                package_name="sample-plugin", module_name="sample_plugin"
            )[0]
            == "main.py"
        )
        assert isinstance(
            plugin_utility.setup_plugin_configuration(
                package_name="sample-plugin", module_name="sample_plugin"
            )[1],
            PluginConfig,
        )
