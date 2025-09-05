import os

from fs_config import get_fs_config
from plugins.plugins.syllabus_weaver import models
from src.utils import DatetimeUtils


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
