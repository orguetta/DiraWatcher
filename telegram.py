import os
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID")
PERSONAL_ID = os.environ.get("TELEGRAM_PERSONAL_ID")

def send_telegram(to: str, text: str):
    if not BOT_TOKEN or not to:
        print("[WARN] Telegram config missing")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": to,
        "text": text
    }
    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        print(f"[OK] Telegram sent to {to}")
    except Exception as e:
        print(f"[ERROR] Telegram failed: {e}")