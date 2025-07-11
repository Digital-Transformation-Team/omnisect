from unittest.mock import patch

from plugins.plugin_use_case_service import PluginUseCase


class TestPluginUseCaseService:
    @patch("plugins.utils.subprocess.check_call")
    @patch("plugins.utils.distributions")
    def test_discover_plugins(self, mock_distributions, mock_check_call):
        mock_distributions.return_value = []
        mock_check_call.return_value = 0
        use_case = PluginUseCase()
        use_case.discover_plugins(reload=True)
        assert len(use_case.modules) == 1
