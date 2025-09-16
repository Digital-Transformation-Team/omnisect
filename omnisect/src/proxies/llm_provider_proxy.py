from openai import OpenAI


class LlmProviderProxy:
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        max_tokens: str = 800,
        temperature: str = 0.7,
    ):
        self._model = model
        self._max_tokens = max_tokens
        self._temperature = temperature
        self._client = OpenAI(api_key=api_key)

    def invoke(self, messages: list[dict[str, str]]) -> str:
        resp = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            max_tokens=self._max_tokens,
            temperature=self._temperature,
        )
        return resp.choices[0].message.content.strip()
