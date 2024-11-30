import os
from datetime import datetime, timedelta
import requests
from pytrends.request import TrendReq
import google.generativeai as genai


class GoogleTrends:
    def __init__(self, hl: str = "pt-BR", tz: int = 360):
        self.pytrends = TrendReq(hl=hl, tz=tz)

    def get_trending_searches(self, region: str = "brazil") -> list:
        try:
            trending_searches_df = self.pytrends.trending_searches(pn=region)
            trending_list = trending_searches_df[0].tolist()
            return trending_list
        except Exception as e:
            print(f"Erro ao obter tendências: {e}")
            return []


class NewsAPIClient:
    def __init__(self, api_key: str, base_url: str = "https://newsapi.org/v2/everything"):
        self.api_key = api_key
        self.base_url = base_url

    def get_news(self, query: str, days_ago: int = 1, sort_by: str = "popularity") -> dict:
        date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        params = {
            "q": query,
            "from": date,
            "to": date,
            "sortBy": sort_by,
            "apiKey": self.api_key,
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a API de notícias: {e}")
            return {}

    def extract_news_content(self, news_data: dict) -> str:
        if "articles" in news_data:
            return "\n".join(
                f"- {article.get('title', 'Sem título')} ({article.get('source', {}).get('name', 'Fonte desconhecida')})"
                for article in news_data.get("articles", [])
            )
        return "Nenhuma notícia disponível."


class GenerativeAIChat:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.generation_config = {
            "temperature": 0.5,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2000,
            "response_mime_type": "text/plain",
        }
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            system_instruction="Você é um assistente que escreve textos jornalísticos claros e objetivos.",
        )
        self.chat_session = None

    def start_chat(self):
        self.chat_session = self.model.start_chat(history=[])

    def generate_article(self, input_text: str) -> str:
        if not self.chat_session:
            raise ValueError("A sessão de chat ainda não foi iniciada. Use start_chat() primeiro.")
        response = self.chat_session.send_message(f"Redija um artigo jornalístico com base nas seguintes informações:\n\n{input_text}")
        return response.text