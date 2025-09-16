# {
#   "text": "string",
#   "language": "russian",
#   "data": { "route": "44.96,-93.27;44.91,-93.5;44.85,-93.46", "product": "meth"
# }
# }

import requests

from plugins.core.iplugin import IPlugin
from plugins.models import PluginInput, PluginOutput
from plugins.plugins.risk_firefly.models.predict_delay import predict_delay


class RiskFirefly(IPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.client_id = "E3WVqjbXmm2kj4h2NxMyM"
        self.client_secret = "MgZ4yv4u3mIj20J5YDNs1WRObEwQyswEr0rQc3mu"
        self._system_prompts = [
            {
                "role": "system",
                "content": """You are a supply chain risk analyst.""",
            }
        ]

    def _fetch_external_data(self, route: str, product: str) -> dict:
        # weather
        try:
            # route = "44.96,-93.27;44.91,-93.5;44.85,-93.46"
            url = "https://data.api.xweather.com/observations/route"
            params = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "p": route,
                "fields": "ob.tempC,ob.windSpeedKPH,ob.humidity",
            }
            weather = requests.get(url, params=params, timeout=10).json()
        except Exception as e:
            self.logger.error(f"Weather API failed: {e}")
            weather = {}
        # currency
        try:
            fx = requests.get(
                "https://api.exchangerate.host/latest?base=USD", timeout=10
            ).json()
        except Exception as e:
            self.logger.error(f"FX API failed: {e}")
            fx = {}

        return {
            "route": route,
            "product": product,
            "weather": weather,
            "fx": fx.get("rates", {}),
        }

    def _is_delay_ml(self, features: dict) -> float:
        try:
            self.logger.debug("_is_delay_ml started")
            # извлекаем простые признаки из погоды
            weather_points = features.get("weather", {}).get("response", [])
            if not weather_points:
                return False
            for p in weather_points:
                ob = p["properties"]["response"]["ob"]
                dl = predict_delay(temp=ob["tempC"], hum=ob["humidity"])
                if dl == 1:
                    return True
            return False
        except Exception as e:
            self.logger.error(f"ML prediction failed: {e}")
            return False

    def _summarize_with_llm(self, data: dict, ml_risk: bool) -> str:
        """
        Используем LLM для объяснения риска
        """
        try:
            prompt = f"""
            Given this data:
            - Route points: {data["route"]}
            - Product: {data["product"]}
            - Weather sample: {data["weather"]}
            - FX (USD->KZT): {data["fx"].get("KZT", "N/A")}
            ML predicted risk: {"delay" if ml_risk else "no delay"}

            Summarize the main risk factors in plain language for a logistics manager.
            """
            messages = self._system_prompts + [
                {
                    "role": "user",
                    "content": prompt,
                },
            ]
            llm_response = self._plugin_services.llm_provider_proxy.invoke(
                messages=messages
            )
            return llm_response
        except Exception as e:
            self.logger.error(f"LLM summarization failed: {e}")
            return f"ML Risk: {ml_risk:.2f} (no LLM summary)"

    def invoke(self, input: PluginInput) -> PluginOutput:
        try:
            data = self._fetch_external_data(input.data["route"], input.data["product"])
            ml_risk = self._is_delay_ml(data)
            summary = self._summarize_with_llm(data, ml_risk)
            result_text = f"Predicted Risk: {ml_risk:.2f}\nSummary: {summary}"

            return PluginOutput(text=result_text, meta=self.meta)
        except Exception as e:
            self.logger.error(f"Invoke failed: {e}")
            return PluginOutput(text=f"Error: {e}", meta=self.meta)
