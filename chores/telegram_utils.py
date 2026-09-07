import requests
from django.conf import settings

def send_telegram_message(chat_id, text):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    if not token:
        print("TELEGRAM_BOT_TOKEN not configured.")
        return False
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Failed to send telegram message: {e}")
        return False
