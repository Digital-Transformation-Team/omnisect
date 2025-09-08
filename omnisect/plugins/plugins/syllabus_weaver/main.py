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
        self, data: dict[str, Any], field: GeneratableField
    ) -> dict[str, Any]:
        if data.get(field.name, None) is None:
            self.logger.info(f"generating missing field: {field.name}")
            messages = self._system_prompts + [
                {"role": "user", "content": field.prompt},
                {
                    "role": "user",
                    "content": f"Course Data: {data['teacher_name']}, {data['course_title']}, {data['course_code']}, {data['course_type']}, {data['course_level']}, {data['course_academic_year']}, {data['course_semester']}, {data['course_credits']}, {data['course_outcomes']}, {data['course_prerequisites']}",
                },
            ]
            value = self._plugin_services.llm_provider_proxy.invoke(messages=messages)
            data[field.name] = ValueParser.parse(
                value, expected_type=field.expected_type
            )
            self.logger.info(f"field {field.name} successfully generated")
        else:
            self.logger.debug(
                f"field {field.name} already present, skipping generation"
            )
        return data

    def _postprocess_fields(self, data: dict[str, Any]) -> dict[str, Any]:
        self.logger.info("_postprocess_fields started")
        for field in self.FIELDS_TO_GENERATE:
            before = data.get(field.name)
            data = self._generate_if_missing(data=data, field=field)
            after = data.get(field.name)
            if before != after:
                self.logger.debug(f"field {field.name} updated during postprocessing")
        self.logger.info("returning from _postprocess_fields")
        return data

    def invoke(self, inp: PluginInput):
        self.logger.info("invoking SyllabusWeaver plugin")
        try:
            context = models.CourseContext(**inp.data)
            enriched_data = self._postprocess_fields(data=context.model_dump())
            context = models.CourseContext(**enriched_data)
            context.set_final_values()
            doc_name = generate_syllabus(context=context)
            self.logger.info(f"syllabus generated successfully: {doc_name}")
            return PluginOutput(file_path=f"{doc_name}")
        except Exception as e:
            self.logger.error(f"error during plugin invocation: {e}", exc_info=True)
            raise
