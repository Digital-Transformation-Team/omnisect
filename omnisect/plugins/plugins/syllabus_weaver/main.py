import datetime
import os

from docxtpl import DocxTemplate

from fs_config import get_fs_config
from plugins.core.iplugin import IPlugin
from plugins.models import PluginInput, PluginOutput
from plugins.plugins.syllabus_weaver import models


class SyllabusWeaver(IPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompts = {}
        self.faq_data = {}

    def invoke(self, inp: PluginInput):
        context = models.CourseContext(**inp.data)
        doc_name = self._generate_syllabus(context=context)
        return PluginOutput(file_path=f"/{doc_name}")

    def _generate_syllabus(self, context: models.CourseContext):
        cfg = get_fs_config()
        templates_dir = os.path.join(
            os.path.join(os.path.dirname(__file__)),
            "templates",
            context.university_name,
        )

        # TODO: Generate on all 3 languages
        doc_name = f"{context.course_code}_{datetime.datetime.now().isoformat(timespec='seconds')}_eng.docx"
        # TODO: Template name must be inside config or as plugin prop
        tmplt = DocxTemplate(os.path.join(templates_dir, "eng.docx"))
        tmplt.render(context.model_dump())

        output_path = os.path.join(cfg.outputs_folder_path, doc_name)
        tmplt.save(output_path)

        return output_path
