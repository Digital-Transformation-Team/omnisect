# {
#   "text": "string",
#   "language": "russian",
#   "data": {
#   "coords": [
#     { "lat": 34.96, "lon": 53.27 },
#     { "lat": 34.96, "lon": 93.27 },
#     { "lat": 34.96, "lon": -93.27 }
#   ]
# }

# }

import datetime

import requests

from plugins.core.iplugin import IPlugin
from plugins.models import PluginInput, PluginOutput


class NewsMoth(IPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._yandex_api_key = "2ebcdfd0-eae8-4393-9d02-3d56d33170e5"
        self._news_api_key = "98fa6210e81b4cdd80dc1d1b033c14d8"

    def _reverse_geocode(self, lat: float, lon: float) -> str:
        try:
            url = "https://geocode-maps.yandex.ru/v1"
            params = {
                "geocode": f"{lon},{lat}",
                "lang": "en-US",
                # 'kind': kwargs.get('kind', ''),
                "format": "json",
                "results": 1,
                "apikey": self._yandex_api_key,
            }
            _meta_data = requests.get(url, params=params, timeout=10).json()
            return (
                _meta_data["response"]["GeoObjectCollection"]["featureMember"][0][
                    "GeoObject"
                ]["metaDataProperty"]["GeocoderMetaData"]
                .get("AddressDetails", {})
                .get("Country", {})
                .get("CountryName")
                if _meta_data
                else "Unknown"
            )
        except Exception as e:
            self.logger.error(f"Geocoding failed for {lat},{lon}: {e}")
            return "Unknown"

    def _fetch_news(self, country: str) -> list[dict]:
        try:
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            formatted = yesterday.strftime("%Y-%m-%d")
            url = f"https://newsapi.org/v2/everything?q={country}&from={formatted}&sortBy=popularity&apiKey={self._news_api_key}"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("articles", [])
            else:
                self.logger.warning(f"News API failed for {country}: {resp.text}")
                return []
        except Exception as e:
            self.logger.error(f"Fetching news failed for {country}: {e}")
            return []

    def _summarize_with_llm(self, country: str, articles: list[dict]) -> str:
        if not articles:
            return f"No significant news found for {country}."

        headlines = [a.get("title") for a in articles[:5] if a.get("title")]
        headlines_text = "\n".join([f"- {h}" for h in headlines])

        messages = [
            {
                "role": "user",
                "content": f"""
        You are a geopolitical risk analyst.
        Summarize main risk factors in {country} based on these recent news headlines:
        {headlines_text}
        """,
            }
        ]
        try:
            llm_response = self._plugin_services.llm_provider_proxy.invoke(
                messages=messages
            )
            return llm_response
        except Exception as e:
            self.logger.error(f"LLM summarization failed: {e}")
            return f"Country {country}: LLM summarization error."

    def invoke(self, input: PluginInput) -> PluginOutput:
        try:
            coords = input.data.get("coords", [])
            if not coords:
                return PluginOutput(text="No coordinates provided", meta=self.meta)

            results = []
            visited = set()

            for point in coords:
                lat = point.get("lat")
                lon = point.get("lon")
                if lat is None or lon is None:
                    continue

                country = self._reverse_geocode(lat, lon)
                if country in visited or country == "Unknown":
                    continue
                visited.add(country)

                articles = self._fetch_news(country)
                summary = self._summarize_with_llm(country, articles)

                results.append(f"### {country=}, {summary=}\n")

            final_text = (
                "\n\n".join(results) if results else "No news summaries available."
            )
            return PluginOutput(text=final_text, meta=self.meta)

        except Exception as e:
            self.logger.error(f"Invoke failed: {e}")
            return PluginOutput(text=f"Error: {e}", meta=self.meta)
