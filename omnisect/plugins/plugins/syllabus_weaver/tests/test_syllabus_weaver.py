import json
from unittest.mock import patch

from plugins.models import PluginInput, PluginOutput
from plugins.plugins.syllabus_weaver.tests import sample_data
from plugins.plugins.syllabus_weaver.tests.plugin_fixtures import PluginFixtures
from tests.fixtures.file_fixtures import FileFixtures


class TestMain(FileFixtures, PluginFixtures):
    def test_invoke_should_return_path_to_outputs(
        self, plugin, fs_config, course_context_builder
    ):
        with patch(
            "plugins.plugins.syllabus_weaver.utils.generate_syllabus"
        ) as mock_generate_syllabus:
            mock_generate_syllabus.return_value = f"{fs_config.outputs_folder_path}/CS101_2024-01-01T12:00:00.000_eng.docx"
            result = plugin.invoke(
                inp=PluginInput(
                    text=None,
                    language="english",
                    data=course_context_builder().model_dump(),
                )
            )
        assert isinstance(result, PluginOutput)
        assert result.text is None
        assert (
            result.file_path
            == f"{fs_config.outputs_folder_path}/CS101_2024-01-01T12:00:00.000_eng.docx"
        )

    def test_invoke_should_generate_data_if_content_data_is_none(
        self, plugin, fs_config, course_context_builder, patch_llm_provider_proxy_invoke
    ):
        patch_llm_provider_proxy_invoke(
            return_value=json.dumps(sample_data.plugin_input["data"]["course_content"])
        )
        with patch(
            "plugins.plugins.syllabus_weaver.utils.generate_syllabus"
        ) as mock_generate_syllabus:
            mock_generate_syllabus.return_value = f"{fs_config.outputs_folder_path}/CS101_2024-01-01T12:00:00.000_eng.docx"
            result = plugin.invoke(
                inp=PluginInput(
                    text=None,
                    language="english",
                    data=course_context_builder(is_content_empty=True).model_dump(),
                )
            )
        assert isinstance(result, PluginOutput)
        assert result.text is None
        assert (
            result.file_path
            == f"{fs_config.outputs_folder_path}/CS101_2024-01-01T12:00:00.000_eng.docx"
        )

    def test_invoke_should_generate_data_if_isc_1_data_is_none(
        self, plugin, fs_config, course_context_builder, patch_llm_provider_proxy_invoke
    ):
        patch_llm_provider_proxy_invoke(
            return_value=json.dumps(
                sample_data.plugin_input["data"]["course_assessment_methods_isc_1"]
            )
        )
        with patch(
            "plugins.plugins.syllabus_weaver.utils.generate_syllabus"
        ) as mock_generate_syllabus:
            mock_generate_syllabus.return_value = f"{fs_config.outputs_folder_path}/CS101_2024-01-01T12:00:00.000_eng.docx"
            result = plugin.invoke(
                inp=PluginInput(
                    text=None,
                    language="english",
                    data=course_context_builder(
                        is_isc_1_assessments_empty=True
                    ).model_dump(),
                )
            )
        assert isinstance(result, PluginOutput)
        assert result.text is None
        assert (
            result.file_path
            == f"{fs_config.outputs_folder_path}/CS101_2024-01-01T12:00:00.000_eng.docx"
        )

    def test_invoke_should_generate_data_if_isc_2_data_is_none(
        self, plugin, fs_config, course_context_builder, patch_llm_provider_proxy_invoke
    ):
        patch_llm_provider_proxy_invoke(
            return_value=json.dumps(
                sample_data.plugin_input["data"]["course_assessment_methods_isc_2"]
            )
        )
        with patch(
            "plugins.plugins.syllabus_weaver.utils.generate_syllabus"
        ) as mock_generate_syllabus:
            mock_generate_syllabus.return_value = f"{fs_config.outputs_folder_path}/CS101_2024-01-01T12:00:00.000_eng.docx"
            result = plugin.invoke(
                inp=PluginInput(
                    text=None,
                    language="english",
                    data=course_context_builder(
                        is_isc_2_assessments_empty=True
                    ).model_dump(),
                )
            )
        assert isinstance(result, PluginOutput)
        assert result.text is None
        assert (
            result.file_path
            == f"{fs_config.outputs_folder_path}/CS101_2024-01-01T12:00:00.000_eng.docx"
        )
