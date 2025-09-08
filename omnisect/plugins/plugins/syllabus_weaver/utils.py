import json
import os
from typing import Any

from fs_config import get_fs_config
from plugins.plugins.syllabus_weaver import models
from src.utils import DatetimeUtils


class ValueParser:
    @staticmethod
    def parse(value: str, expected_type: str) -> Any:
        if expected_type == "string":
            return value.strip()
        if expected_type in ["integer", "number"]:
            try:
                return int(value) if expected_type["integer"] else float(value)
            except ValueError as err:
                raise ValueError(f"Expected {expected_type}, got {value}") from err
        if expected_type in ["array", "object", "dict", "list"]:
            try:
                return json.loads(value)
            except json.JSONDecodeError as err:
                raise ValueError(
                    f"Expected JSON for {expected_type}, got {value}"
                ) from err


def generate_syllabus(context: models.CourseContext):
    from docxtpl import DocxTemplate

    cfg = get_fs_config()
    # TODO: Generate on all 3 languages
    doc_name = f"{context.course_code}_{DatetimeUtils.now_iso_str()}_eng.docx"
    templates_dir = os.path.join(
        os.path.join(os.path.dirname(__file__)),
        "templates",
        context.university_name,
    )
    tmplt = DocxTemplate(os.path.join(templates_dir, "eng.docx"))
    tmplt.render(context.model_dump())

    output_path = os.path.join(cfg.outputs_folder_path, doc_name)
    tmplt.save(output_path)

    return output_path
