from dataclasses import dataclass
from typing import Any, ClassVar

from plugins.core.iplugin import IPlugin
from plugins.models import PluginInput, PluginOutput
from plugins.plugins.syllabus_weaver import models
from plugins.plugins.syllabus_weaver.utils import ValueParser, generate_syllabus


@dataclass
class GeneratableField:
    name: str
    prompt: str
    expected_type: str


class SyllabusWeaver(IPlugin):
    FIELDS_TO_GENERATE: ClassVar[list[GeneratableField]] = [
        GeneratableField(
            name="course_content",
            prompt="""Generate a valid value for the field `course_content`.
This must be a JSON array of exactly 15 objects, each describing one week of the course.
Each object must contain the following keys:
- "week": integer from 1 to 15, sequential without gaps or duplicates.
- "topic": short descriptive title of the week’s content, consistent with the course context.
- "contract_hours": integer value (3 or 4).
- "sss": integer value (5 or 6).

Business rules:
1. The array must always contain exactly 15 elements.

Constraints:
- Do not output anything except the final JSON array.
- All content must logically align with the course name, description, and objectives.
- Do not include explanations, comments, or formatting beyond the JSON array.
""",
            expected_type="list",
        ),
        GeneratableField(
            name="course_assessment_methods_isc_1",
            prompt="""Generate a valid JSON array for the field `course_assessment_methods_isc_1`.
Each element must represent one assessment activity with the following keys:
- "week": integer, the course week number (must correspond to actual course weeks 1-7).
- "title": short name of the assignment (e.g., "Task 1").
- "topic": topic(s) of the course covered during that week or weeks.
- "form": type of assessment that is appropriate for the content of that week (e.g., "Written work", "Practical task (on the computer)", "Project with defence", "Presentation", "Quiz", etc.).
- "points": integer, maximum points for this assessment (total across all tasks should be 100).
- "weight": integer, percentage contribution of this assessment to the final ISC 1 grade (sum of all weights must be exactly 100).

Business rules:
1. The array must contain exactly 3 assessments.
2. Weights must sum to exactly 100.
3. Assessments must align with the course content and weeks (topics must come directly from the course_content field).
4. The form of assessment must logically match the nature of the topics (e.g., theory → written test, practical topic → computer task, project-related topic → project with defence).
5. Points must reflect the relative difficulty or scope of each assignment.

Constraints:
- Do not output anything except the JSON array.
- Do not include explanations, comments, or extra formatting beyond valid JSON.
""",
            expected_type="list",
        ),
        GeneratableField(
            name="course_assessment_methods_isc_2",
            prompt="""Generate a valid JSON array for the field `course_assessment_methods_isc_2`.
Each element must represent one assessment activity with the following keys:
- "week": integer, the course week number (must correspond to actual course weeks 8-15).
- "title": short name of the assignment (e.g., "Task 4").
- "topic": topic(s) of the course covered during that week or weeks.
- "form": type of assessment that is appropriate for the content of that week (e.g., "Written work", "Practical task (on the computer)", "Project with defence", "Presentation", "Quiz", etc.).
- "points": integer, maximum points for this assessment (total across all tasks should be 100).
- "weight": integer, percentage contribution of this assessment to the final ISC 2 grade (sum of all weights must be exactly 100).

Business rules:
1. The array must contain exactly 3 assessments.
2. Weights must sum to exactly 100.
3. Assessments must align with the course content and weeks (topics must come directly from the course_content field).
4. The form of assessment must logically match the nature of the topics (e.g., theory → written test, practical topic → computer task, project-related topic → project with defence).
5. Points must reflect the relative difficulty or scope of each assignment.

Constraints:
- Do not output anything except the JSON array.
- Do not include explanations, comments, or extra formatting beyond valid JSON.
""",
            expected_type="list",
        ),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._system_prompts = [
            {
                "role": "system",
                "content": """You are tasked with generating specific academic fields for a course.
                        Always base your answers on the existing course context (such as course name, description, objectives, and other provided details).
                        Your response must contain only the valid content for the requested field, without any additional explanations, comments, or formatting.
                        If course context is incomplete, infer logically but never contradict the given data.""",
            }
        ]

    def _generate_if_missing(
        self, course_context: models.CourseContext, field: GeneratableField
    ) -> dict[str, Any]:
        if getattr(course_context, field.name) is None:
            messages = self._system_prompts + [
                {"role": "user", "content": field.prompt},
                {
                    "role": "user",
                    "content": f"Course Data: {course_context.teacher_name=}, {course_context.course_title=}, {course_context.course_code=}, {course_context.course_type=}, {course_context.course_level=}, {course_context.course_academic_year=}, {course_context.course_semester=}, {course_context.course_credits=}, {course_context.course_outcomes=}, {course_context.course_prerequisites=}",
                },
            ]
            # invoke openai api
            value = self._plugin_services.llm_provider_proxy.invoke(messages=messages)
            setattr(
                course_context,
                field.name,
                ValueParser.parse(value, expected_type=field.expected_type),
            )
        return course_context

    def _postprocess_fields(
        self, course_context: models.CourseContext
    ) -> models.CourseContext:
        for field in self.FIELDS_TO_GENERATE:
            data = self._generate_if_missing(
                course_context=course_context,
                field=field,
            )
        return data

    def invoke(self, inp: PluginInput):
        # send request to openapi client for field generation if course context field is marked as "must be generated"
        context = models.CourseContext(**inp.data)
        context = self._postprocess_fields(course_context=context)
        # final validation
        doc_name = generate_syllabus(context=context)
        return PluginOutput(file_path=f"{doc_name}")
