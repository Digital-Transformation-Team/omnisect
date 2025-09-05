from plugins.core.iplugin import IPlugin
from plugins.models import PluginInput, PluginOutput
from plugins.plugins.syllabus_weaver import models
from plugins.plugins.syllabus_weaver.utils import generate_syllabus


class SyllabusWeaver(IPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompts = {}
        self.faq_data = {}

    def invoke(self, inp: PluginInput):
        context = models.CourseContext(**inp.data)
        doc_name = generate_syllabus(context=context)
        return PluginOutput(file_path=f"{doc_name}")
