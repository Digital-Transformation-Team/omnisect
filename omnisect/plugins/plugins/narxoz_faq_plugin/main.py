import json
import os

from plugins.core.iplugin import IPlugin
from plugins.models import PluginInput, PluginOutput


class NarxozFaqPlugin(IPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompts = {}
        self.faq_data = {}
        self.load_configurations()

    def load_configurations(self):
        """Load prompts, greetings, and FAQ data from files."""
        base_dir = os.path.join(os.path.dirname(__file__), "config")
        try:
            with open(os.path.join(base_dir, "prompts.json"), encoding="utf-8") as f:
                self.prompts = json.load(f)

            with open(os.path.join(base_dir, "greetings.json"), encoding="utf-8") as f:
                self.greetings = json.load(f)

            with open(os.path.join(base_dir, "faq_data.json"), encoding="utf-8") as f:
                self.faq_data = json.load(f)
            self.logger.info("Configuration files loaded successfully")
        except Exception as e:
            self.logger.error(f"Error loading configuration files: {e}")
            raise

    def invoke(self, inp: PluginInput) -> PluginOutput:
        """Generate response using OpenAI with context from memory and FAQ data."""
        try:
            # Get appropriate system prompt based on language
            system_prompt = self.prompts.get(inp.language, self.prompts["russian"])

            # Add FAQ knowledge base to prompt
            faq_context = "\n\nБаза знаний (FAQ):\n"
            for faq in self.faq_data.get("questions", []):
                faq_context += f"Вопрос: {faq['question']}\nОтвет: {faq['answer']}\n\n"

            messages = [
                {
                    "role": "system",
                    "content": system_prompt + faq_context,
                },
                {
                    "role": "user",
                    "content": f"Ответь на следующий вопрос на языке {inp.language}: {inp.text}",
                },
            ]
            resp = self._plugin_services.openai_client.chat.completions.create(
                model="gpt-4o-mini", messages=messages, max_tokens=800, temperature=0.7
            )
            return PluginOutput(text=resp.choices[0].message.content.strip())

        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            error_messages = {
                "russian": "Извините, произошла ошибка. Попробуйте позже или обратитесь в службу поддержки.",
                "kazakh": "Кешіріңіз, қате орын алды. Кейінірек қайталап көріңіз немесе қолдау қызметіне хабарласыңыз.",
                "english": "Sorry, an error occurred. Please try again later or contact support.",
            }
            return PluginOutput(
                text=error_messages.get(inp.language, error_messages["russian"])
            )
