"""
Cliente para integração com API do Ploomes CRM
"""
import requests
from datetime import timezone, datetime, timedelta
from typing import List, Dict
import json

from config import PLOOMES_USER_KEY, DAYS_TO_SEARCH, MAX_INTERACTIONS


class PloomesClient:
    def __init__(self, user_key: str, base_url: str = 'https://api2.ploomes.com'):
        self.user_key = user_key
        self.base_url = base_url
        self.headers = {
            'User-Key': user_key,
            'Content-Type': 'application/json'
        }

    def test_connection(self) -> bool:
        """Testa conexão com a API"""
        try:
            response = requests.get(
                f"{self.base_url}/Users",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def get_interactions(self, days: int = 7, max_results: int = 100) -> List[Dict]:
        """Busca interações dos últimos N dias"""
        # Pega a data em UTC corretamente
        start_date_utc = (datetime.now(timezone.utc) - timedelta(days=days))
        date_filter = start_date_utc.strftime('%Y-%m-%dT%H:%M:%SZ')

        url = f"{self.base_url}/InteractionRecords"
        params = {
            '$filter': f"Date ge {date_filter}",
            '$orderby': 'Date desc',
            '$top': max_results,
            '$select': 'Date,TypeId,Content'
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            data = response.json()
            return data.get('value', [])

        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar interações: {e}")
            return []

    def format_interactions(self, interactions: List[Dict]):
        """Formata interações para análise"""
        formatted = []

        for interaction in interactions:
            formatted_interaction = {
                'data': interaction.get('Date', ''),
                'tipo_id': interaction.get('TypeId'),
                'conteudo': interaction.get('Content', 'Sem conteúdo'),
            }
            formatted.append(formatted_interaction)

        return json.dumps(formatted, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    ploomes = PloomesClient(PLOOMES_USER_KEY)

    interactions = ploomes.get_interactions(DAYS_TO_SEARCH, MAX_INTERACTIONS)
    formatted_data = ploomes.format_interactions(interactions)
