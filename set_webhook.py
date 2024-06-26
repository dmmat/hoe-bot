import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
params = {
    "url": f'{WEBHOOK_URL}/tg-webhook'
}

response = requests.post(url, params=params)
print(response.json())
