from unittest.mock import patch

from plugins.models import PluginInput, PluginOutput
from plugins.plugins.syllabus_weaver.tests.plugin_fixtures import PluginFixtures
from tests.fixtures.file_fixtures import FileFixtures


class TestMain(FileFixtures, PluginFixtures):
    def test_invoke_should_return_path_to_outputs(
        self, plugin, fs_config, sample_course_context
    ):
        with patch(
            "plugins.plugins.syllabus_weaver.utils.generate_syllabus"
        ) as mock_generate_syllabus:
            mock_generate_syllabus.return_value = f"{fs_config.outputs_folder_path}/CS101_2024-01-01T12:00:00.000_eng.docx"
            result = plugin.invoke(
                inp=PluginInput(
                    text=None,
                    language="english",
                    data=sample_course_context.model_dump(),
                )
            )
        assert isinstance(result, PluginOutput)
        assert result.text is None
        assert (
            result.file_path
            == f"{fs_config.outputs_folder_path}/CS101_2024-01-01T12:00:00.000_eng.docx"
        )
