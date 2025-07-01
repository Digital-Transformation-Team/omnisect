from plugins.models import Meta
from plugins.core.iplugin import IPlugin


class SamplePlugin(IPlugin):
    def __init__(self, logger):
        super().__init__(logger)
        self.meta = Meta(
            name="Sample Plugin",
            description="sample plugin template",
            version="1.1.1",
        )

    def invoke(self, text: str) -> str:
        self._logger.debug(f"Text: {text} -> {self.meta}")
        return text
