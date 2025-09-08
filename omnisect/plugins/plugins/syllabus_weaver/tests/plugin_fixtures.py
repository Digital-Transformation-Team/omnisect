import os

import pytest

from plugins.helpers import FileSystem
from plugins.models import PluginConfig, PluginRunTimeOption
from plugins.plugins.syllabus_weaver.main import SyllabusWeaver
from plugins.plugins.syllabus_weaver.models import (
    AssessmentMethod,
    CourseContentWeek,
    CourseContext,
    Teacher,
)
from plugins.utils import PluginUtility
from tests.base_test import BaseTest


class PluginFixtures(BaseTest):
    @pytest.fixture
    def patch_file_system_get_plugins_directory(self, monkeypatch):
        def _get_plugins_directory(*args, **kwargs):
            return os.path.join(FileSystem.get_base_dir(), "plugins")

        monkeypatch.setattr(FileSystem, "get_plugins_directory", _get_plugins_directory)

    @pytest.fixture(autouse=True)
    def setup_plugin(self, logger, patch_file_system_get_plugins_directory):
        p_utils = PluginUtility(logger=logger)
        p_utils.setup_plugin_configuration(
            package_name="plugins", module_name="syllabus_weaver"
        )

    @pytest.fixture
    def plugin(self, plugin_services, logger):
        return SyllabusWeaver(
            logger=logger,
            plugin_services=plugin_services,
            plugin_config=PluginConfig(
                name="Syllabus Weaver",
                alias="syllabus-weaver",
                creator="test-bl1nkker",
                runtime=PluginRunTimeOption(main="main.py", tests=None),
                repository="github.com/weaver-repo",
                description="sample-description",
                version="0.0.1",
                requirements=None,
                instructions=None,
            ),
        )

    @pytest.fixture
    def course_context_builder(self):
        def _gen(university_name: str = "narxoz"):
            return CourseContext(
                teacher_name="Dr. John Smith",
                university_name=university_name,
                course_title="Introduction to 500 bucks",
                course_code="CS101",
                course_type="Compulsory",
                course_level="Bachelor - first cycle",
                course_academic_year=2025,
                course_semester="Fall",
                course_credits=6,
                course_teachers=[
                    Teacher(
                        title="Prof.",
                        fullname="John Smith",
                        email="john.smith@example.com",
                    ),
                    Teacher(
                        title="Dr.",
                        fullname="Alice Johnson",
                        email="alice.johnson@example.com",
                    ),
                ],
                course_outcomes="By the end of the course, students will be able to understand the fundamentals of AI, apply search algorithms, analyze data using machine learning techniques, and critically evaluate AI applications.",
                course_prerequisites="Basic knowledge of programming in Python and introductory linear algebra.",
                course_content=[
                    CourseContentWeek(
                        week=1, topic="Introduction to AI", contract_hours=2, sss=1
                    ),
                    CourseContentWeek(
                        week=2,
                        topic="History and Applications",
                        contract_hours=2,
                        sss=1,
                    ),
                    CourseContentWeek(
                        week=3, topic="Search Algorithms I", contract_hours=2, sss=1
                    ),
                    CourseContentWeek(
                        week=4, topic="Search Algorithms II", contract_hours=2, sss=1
                    ),
                    CourseContentWeek(
                        week=5, topic="Game Playing", contract_hours=2, sss=1
                    ),
                    CourseContentWeek(
                        week=6,
                        topic="Knowledge Representation",
                        contract_hours=2,
                        sss=1,
                    ),
                    CourseContentWeek(
                        week=7, topic="Reasoning", contract_hours=2, sss=1
                    ),
                    CourseContentWeek(
                        week=8, topic="Planning", contract_hours=2, sss=1
                    ),
                    CourseContentWeek(
                        week=9, topic="Uncertainty in AI", contract_hours=2, sss=1
                    ),
                    CourseContentWeek(
                        week=10,
                        topic="Machine Learning Basics",
                        contract_hours=2,
                        sss=1,
                    ),
                    CourseContentWeek(
                        week=11, topic="Supervised Learning", contract_hours=2, sss=1
                    ),
                    CourseContentWeek(
                        week=12, topic="Unsupervised Learning", contract_hours=2, sss=1
                    ),
                    CourseContentWeek(
                        week=13, topic="Neural Networks", contract_hours=2, sss=1
                    ),
                    CourseContentWeek(
                        week=14, topic="Ethics in AI", contract_hours=2, sss=1
                    ),
                    CourseContentWeek(
                        week=15,
                        topic="Course Review and Project Presentations",
                        contract_hours=2,
                        sss=1,
                    ),
                ],
                course_content_contact_hours_total=30,
                course_content_sss_total=15,
                course_required_literature=[
                    "Russell, S., and Norvig, P. (2021). Artificial Intelligence: A Modern Approach."
                ],
                course_recommended_literature=[
                    "Goodfellow, I., Bengio, Y., and Courville, A. (2016). Deep Learning."
                ],
                course_internet_sources=[
                    "https://ai.google",
                    "https://towardsdatascience.com",
                ],
                course_other_sources=["Lecture slides provided by instructor"],
                course_languages=["English language"],
                course_assessment_methods_isc_1=[
                    AssessmentMethod(
                        week=3,
                        title="Quiz 1",
                        topic="Search Algorithms",
                        form="Quiz",
                        points=10,
                        weight=20,
                    ),
                    AssessmentMethod(
                        week=6,
                        title="Midterm Exam",
                        topic="Reasoning and Search",
                        form="Exam",
                        points=30,
                        weight=40,
                    ),
                    AssessmentMethod(
                        week=10,
                        title="Project Proposal",
                        topic="AI Applications",
                        form="Presentation",
                        points=20,
                        weight=40,
                    ),
                ],
                course_assessment_methods_isc_2=[
                    AssessmentMethod(
                        week=12,
                        title="Quiz 2",
                        topic="Machine Learning",
                        form="Quiz",
                        points=10,
                        weight=20,
                    ),
                    AssessmentMethod(
                        week=14,
                        title="Project Report",
                        topic="Applied AI",
                        form="Report",
                        points=30,
                        weight=40,
                    ),
                    AssessmentMethod(
                        week=15,
                        title="Final Presentation",
                        topic="AI Project",
                        form="Presentation",
                        points=20,
                        weight=40,
                    ),
                ],
                course_assessment_final_exam_topic="Comprehensive evaluation of AI techniques",
                course_assessment_final_exam_form="Written exam",
            )

        return _gen

    @pytest.fixture
    def sample_course_context(self, course_context_builder):
        return course_context_builder()
