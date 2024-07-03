## Можете встановити з deta та налаштувати просто конфіг
https://deta.space/discovery/@dmat/hoebot



### Створіть та активуйте віртуальне середовище (рекомендовано):

```
python -m venv venv
source venv/bin/activate   # Для Linux або MacOS
venv\Scripts\activate      # Для Windows
```

### Встановіть бібліотеки з файлу requirements.txt:

```pip install -r requirements.txt```

### Створіть файл .env з вашими змінними оточення:

STREET_ID та HOUSE потрібно взяти звідси - https://hoe.com.ua/shutdown/queue

```
TELEGRAM_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
WEBHOOK_URL=
TELEGRAM_TOKEN=
WEBHOOK_URL=
ROUTER_URL=
STREET_ID=
HOUSE=
ALLOWED_CHAT_IDS=
NOTIFY_CHAT_IDS=
DETA_PROJECT_KEY=
```

### Запустіть set_webhook.py для встановлення вебхука:
python set_webhook.py
