"""
Configurações centralizadas do projeto
"""
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Ploomes
PLOOMES_USER_KEY = os.getenv('PLOOMES_USER_KEY')
PLOOMES_BASE_URL = 'https://api2.ploomes.com'

# Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Z-API
ZAPI_INSTANCE = os.getenv('ZAPI_INSTANCE')
ZAPI_TOKEN = os.getenv('ZAPI_TOKEN')
ZAPI_SECURITY_TOKEN= os.getenv('ZAPI_SECURITY_TOKEN')
ZAPI_BASE_URL = f'https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}'

# WhatsApp
WHATSAPP_NUMBER = os.getenv('WHATSAPP_NUMBER')

DAYS_TO_SEARCH = int(os.getenv('DAYS_TO_SEARCH', 7))
MAX_INTERACTIONS = int(os.getenv('MAX_INTERACTIONS', 50))

def validate_config():
    """Valida se todas as configurações necessárias estão presentes"""
    missing = []

    if not PLOOMES_USER_KEY:
        missing.append('PLOOMES_USER_KEY')

    if not GEMINI_API_KEY:
        missing.append('GEMINI_API_KEY')

    if not ZAPI_INSTANCE:
        missing.append('ZAPI_INSTANCE')

    if not ZAPI_TOKEN:
        missing.append('ZAPI_TOKEN')

    if not WHATSAPP_NUMBER:
        missing.append('WHATSAPP_NUMBER')

    if missing:
        raise ValueError(f"Configurações obrigatórias ausentes: {', '.join(missing)}")

    return True


if __name__ == "__main__":
    try:
        validate_config()
        print("Todas as configurações estão corretas!")
    except ValueError as e:
        print(f" {e}")