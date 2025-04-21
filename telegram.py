import os
import requests
import re

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID")
PERSONAL_ID = os.environ.get("TELEGRAM_PERSONAL_ID")

MAX_LENGTH = 4096

def escape_markdown(text: str) -> str:
    """
    Escapes Telegram MarkdownV2 reserved characters.
    """
    escape_chars = r"_*[]()~`>#+-=|{}.!\\"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

def send_telegram(to: str, text: str, markdown: bool = False):
    if not BOT_TOKEN or not to:
        print("[WARN] Telegram config missing")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    if markdown:
        text = escape_markdown(text)

    chunks = [text[i:i+MAX_LENGTH] for i in range(0, len(text), MAX_LENGTH)]

    for chunk in chunks:
        payload = {
            "chat_id": to,
            "text": chunk
        }

        if markdown:
            payload["parse_mode"] = "MarkdownV2"

        try:
            res = requests.post(url, json=payload)
            res.raise_for_status()
            print(f"[OK] Telegram sent to {to} ({len(chunk)} chars)")
        except Exception as e:
            print(f"[ERROR] Telegram failed: {e}")
            print(f"[DEBUG] Response: {res.status_code} – {res.text}")