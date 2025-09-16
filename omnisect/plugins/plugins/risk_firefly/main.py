# {
#   "text": "string",
#   "language": "russian",
#   "data": { "route": "44.96,-93.27;44.91,-93.5;44.85,-93.46", "product": "meth"
# }
# }

import joblib
import requests

from plugins.core.iplugin import IPlugin
from plugins.models import PluginInput, PluginOutput


class RiskFirefly(IPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.model = joblib.load("models/risk_model.pkl")
        except Exception:
            self.model = None
            self.logger.warning("ML model not found. Predictions will default to 0.5")

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
                "fields": "ob.tempC,ob.windSpeedKPH",
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

    def _predict_risk_ml(self, features: dict) -> float:
        if not self.model:
            return 0.5
        try:
            # извлекаем простые признаки из погоды
            weather_points = features.get("weather", {}).get("response", [])
            if not weather_points:
                return 0.5

            temps = []
            winds = []
            for p in weather_points:
                ob = p.get("properties", {}).get("response", {}).get("ob", {})
                if "tempC" in ob:
                    temps.append(ob["tempC"])
                if "windSpeedKPH" in ob:
                    winds.append(ob["windSpeedKPH"])

            avg_temp = sum(temps) / len(temps) if temps else 20
            avg_wind = sum(winds) / len(winds) if winds else 5
            usd_kzt = features.get("fx", {}).get("KZT", 480)

            X = [avg_temp, avg_wind, usd_kzt]
            prob = self.model.predict_proba([X])[0][1]
            return float(prob)
        except Exception as e:
            self.logger.error(f"ML prediction failed: {e}")
            return 0.5

    def _summarize_with_llm(self, data: dict, ml_risk: float) -> str:
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
            ML predicted risk: {ml_risk:.2f}

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
            ml_risk = self._predict_risk_ml(data)
            summary = self._summarize_with_llm(data, ml_risk)
            result_text = f"Predicted Risk: {ml_risk:.2f}\nSummary: {summary}"

            return PluginOutput(text=result_text, meta=self.meta)
        except Exception as e:
            self.logger.error(f"Invoke failed: {e}")
            return PluginOutput(text=f"Error: {e}", meta=self.meta)
