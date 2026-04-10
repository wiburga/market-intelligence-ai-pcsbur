import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('BLACKBOX_API_KEY')
# Agregar prefijo sk-
full_key = f'sk-{api_key}' if not api_key.startswith('sk-') else api_key

url = 'https://api.blackbox.ai/chat/completions'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {full_key}'
}

payload = {
    'messages': [{'role': 'user', 'content': 'Hola'}],
    'model': 'blackboxai',
    'stream': False
}

print(f'Testing with sk- prefix on api.blackbox.ai...')
response = requests.post(url, headers=headers, json=payload, timeout=30)
print(f'Status: {response.status_code}')
print(f'Content: {response.text[:200]}')
