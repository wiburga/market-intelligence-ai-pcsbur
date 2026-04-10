import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('BLACKBOX_API_KEY')
# Probar con y sin prefijo 'bb_' si no lo tiene
# api_key = f'bb_{api_key}' if not api_key.startswith('bb_') else api_key

url = 'https://www.blackbox.ai/api/chat'

payload = {
    'messages': [{'role': 'user', 'content': 'Hola'}],
    'model': 'blackbox-search',
    'stream': False,
    'apiKey': api_key  # Probando esto
}

print(f'Testing with apiKey in body...')
response = requests.post(url, json=payload, timeout=30)
print(f'Status: {response.status_code}')
print(f'Content: {response.text[:200]}')
