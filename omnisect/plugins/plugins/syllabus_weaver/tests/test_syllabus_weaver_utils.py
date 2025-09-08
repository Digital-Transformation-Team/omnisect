import os

from docxtpl import DocxTemplate

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

    def test_generate_syllabus_should_update_template(
        self, sample_course_context, fs_config, cleanup_files
    ):
        generate_syllabus(context=sample_course_context)
        doc = DocxTemplate(
            f"{fs_config.outputs_folder_path}/CS101_2024-01-01T12:00:00.000_eng.docx"
        )
        xml = doc.get_docx()._body._body.xml
        assert "Dr. John Smith" in xml
        assert "Introduction to 500 bucks" in xml
        assert "CS101" in xml
        assert "Compulsory" in xml
        assert "Bachelor - first cycle" in xml
        assert "2025" in xml
        assert "Fall" in xml
        assert sample_course_context.course_outcomes in xml
        assert sample_course_context.course_prerequisites in xml
        assert sample_course_context.course_assessment_final_exam_topic in xml
        assert sample_course_context.course_assessment_final_exam_form in xml
        for item in sample_course_context.course_content:
            assert item.topic in xml
        for item in sample_course_context.course_assessment_methods_isc_1:
            assert item.topic in xml
        for item in sample_course_context.course_assessment_methods_isc_2:
            assert item.topic in xml
        for lit in sample_course_context.course_required_literature:
            assert lit in xml
        for lit in sample_course_context.course_recommended_literature:
            assert lit in xml
        for lit in sample_course_context.course_internet_sources:
            assert lit in xml
        for lit in sample_course_context.course_other_sources:
            assert lit in xml
        for lang in sample_course_context.course_languages:
            assert lang in xml
