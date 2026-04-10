import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('BLACKBOX_API_KEY')
# Agregar prefijo bb- si no lo tiene
full_key = f'bb-{api_key}' if not api_key.startswith('bb-') else api_key

url = 'https://www.blackbox.ai/api/chat'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {full_key}'
}

payload = {
    'messages': [{'role': 'user', 'content': 'Hola'}],
    'model': 'blackbox-search',
    'stream': False
}

print(f'Testing with bb- prefix...')
response = requests.post(url, headers=headers, json=payload, timeout=30)
print(f'Status: {response.status_code}')
print(f'Content: {response.text[:200]}')
