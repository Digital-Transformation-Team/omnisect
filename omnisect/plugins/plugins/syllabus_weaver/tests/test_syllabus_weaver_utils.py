import os

from plugins.plugins.syllabus_weaver.tests.plugin_fixtures import PluginFixtures
from plugins.plugins.syllabus_weaver.utils import generate_syllabus
from tests.fixtures.file_fixtures import FileFixtures


class TestUtils(FileFixtures, PluginFixtures):
    def test_generate_syllabus_should_return_generated_file_path(
        self, sample_course_context, fs_config, cleanup_files
    ):
        result = generate_syllabus(context=sample_course_context)
        assert (
            result
            == f"{fs_config.outputs_folder_path}/CS101_2024-01-01T12:00:00.000_eng.docx"
        )

    def test_generate_syllabus_should_actual_generate_new_file(
        self, sample_course_context, fs_config, cleanup_files
    ):
        generate_syllabus(context=sample_course_context)
        assert os.path.isfile(
            f"{fs_config.outputs_folder_path}/CS101_2024-01-01T12:00:00.000_eng.docx"
        )
