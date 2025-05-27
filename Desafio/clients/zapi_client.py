import requests
from typing import Dict, Any


class ZAPIClient:
    def __init__(self, instance: str, token: str, client_token: str):
        self.instance = instance
        self.token = token
        self.client_token = client_token

        self.base_url = f'https://api.z-api.io/instances/{self.instance}/token/{self.token}'

        self.headers = {
            'Client-Token': self.client_token,
            'Content-Type': 'application/json'
        }

    def test_connection(self) -> bool:
        """Testa se WhatsApp está conectado"""
        try:
            url = f"{self.base_url}/status"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('connected', False)
            return False
        except Exception:
            return False

    def send_message(self, phone: str, message: str) -> Dict[str, Any]:
        """Envia mensagem via WhatsApp"""
        url = f"{self.base_url}/send-text"

        payload = {
            "phone": phone,
            "message": message
        }

        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            response.raise_for_status()

            return {
                'success': True,
                'data': response.json()
            }

        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_status(self) -> Dict[str, Any]:
        """Obtém status da conexão"""
        try:
            url = f"{self.base_url}/status"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}
