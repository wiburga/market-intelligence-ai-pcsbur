import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('BLACKBOX_API_KEY')
full_key = f'sk-{api_key}' if not api_key.startswith('sk-') else api_key

url = 'https://api.blackbox.ai/v1/models'
headers = {'Authorization': f'Bearer {full_key}'}

print('Fetching models...')
response = requests.get(url, headers=headers, timeout=30)
print(f'Status: {response.status_code}')
print(f'Content: {response.text[:500]}')
