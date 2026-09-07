import os
import requests
from django.conf import settings

def send_telegram_message(chat_id: str, text: str) -> bool:
    """
    Send a message to a Telegram chat using the bot API.
    Returns True if successful, False otherwise.
    """
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    if not token:
        print("Warning: TELEGRAM_BOT_TOKEN is not set in settings.")
        return False
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Error sending Telegram message: {e}")
        return False
