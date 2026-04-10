import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BLACKBOX_API_KEY")
url = "https://www.blackbox.ai/api/chat"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "messages": [{"role": "user", "content": "Hola, responde solo con la palabra 'test'"}],
    "model": "blackbox-search",
    "stream": False
}

print(f"URL: {url}")
print(f"Headers: {headers}")

try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: '{response.text}'")
    try:
        print(f"JSON: {response.json()}")
    except:
        print("Response is not JSON")
except Exception as e:
    print(f"Error: {e}")
