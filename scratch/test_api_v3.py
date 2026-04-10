import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('BLACKBOX_API_KEY')
# Prueba con endpoint de la API oficial
url = 'https://api.blackbox.ai/chat/completions'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

payload = {
    'messages': [{'role': 'user', 'content': 'Hola'}],
    'model': 'blackboxai',
    'stream': False
}

print(f'Testing with endpoint: {url}')
try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f'Status: {response.status_code}')
    print(f'Content: {response.text[:200]}')
except Exception as e:
    print(f'Error: {e}')
