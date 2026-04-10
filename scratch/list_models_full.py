import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('BLACKBOX_API_KEY')
full_key = f'sk-{api_key}' if not api_key.startswith('sk-') else api_key

url = 'https://api.blackbox.ai/v1/models'
headers = {'Authorization': f'Bearer {full_key}'}

response = requests.get(url, headers=headers, timeout=30)
models = [m['id'] for m in response.json()['data']]
for m in models:
    print(m)
