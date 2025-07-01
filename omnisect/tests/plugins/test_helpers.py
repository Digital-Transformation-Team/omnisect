from tests.fixtures.file_fixtures import FileFixtures
from plugins.helpers import FileSystem


class TestHelpers(FileFixtures):
    def test_file_system_get_plugins_directory(self):
        assert FileSystem.get_plugins_directory().endswith("plugins/plugins")

    def test_file_system_load_configuration(self, fs_config):
        assert FileSystem.load_configuration(
            name="configuration.yaml",
            config_directory=fs_config.test_data_path,
        ) == {
            "logging": {"level": "DEBUG"},
            "plugins": ["advance-plugin", "sample-plugin"],
            "registry": {
                "name": "",
                "repository": "",
                "tag": "latest",
                "url": "https://github.com/{name}/{repository}/releases/download/{tag}",
            },
        }
