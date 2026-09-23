import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
from urllib.parse import quote
from pathlib import Path
from telegram import send_telegram, CHANNEL_ID, PERSONAL_ID
from csv_writer import write_projects_to_csv

BASE_URL = "https://www.dira.moch.gov.il/api/Invoker"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.dira.moch.gov.il/ProjectsList"
}

STATE_PATH = Path("state.json")
REQUEST_TIMEOUT = (10, 30)


def build_session() -> requests.Session:
    """Create an HTTP session that retries transient API failures."""
    retry = Retry(
        total=4,
        connect=4,
        read=4,
        status=4,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
    )
    session = requests.Session()
    session.headers.update(HEADERS)
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session

def fetch_projects(status: int, session: requests.Session) -> list[dict]:
    """Fetch all project pages for given status (2=upcoming, 4=open)"""
    all_projects = []
    page = 1

    while True:
        raw_param = f"?ProjectStatus={status}&Entitlement=1&PageNumber={page}&PageSize=50&IsInit=false"
        encoded_param = quote(raw_param, safe="")
        url = f"{BASE_URL}?method=Projects&param={encoded_param}"

        res = session.get(url, timeout=REQUEST_TIMEOUT)
        res.raise_for_status()
        page_data = res.json().get("ProjectItems", [])

        if not page_data:
            break

        all_projects.extend(page_data)
        page += 1

    return all_projects

def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"open": [], "upcoming": []}

def save_state(state: dict):
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False))

def extract_ids(projects: list[dict]) -> list[str]:
    return [str(p["ProjectNumber"]) for p in projects]

def check_new_projects():
    session = build_session()
    try:
        current_open = fetch_projects(4, session)
        current_upcoming = fetch_projects(2, session)
    except (requests.RequestException, ValueError) as exc:
        # Preserve state.json and the CSV when the upstream API is temporarily unavailable.
        warning = f"⚠️ בדיקת פרויקטים נכשלה זמנית מול API משרד השיכון: {exc}"
        print(warning)
        send_telegram(PERSONAL_ID, warning)
        return

    current_state = {
        "open": extract_ids(current_open),
        "upcoming": extract_ids(current_upcoming),
    }

    previous_state = load_state()

    new_open = [p for p in current_open if str(p["ProjectNumber"]) not in previous_state["open"]]
    new_upcoming = [p for p in current_upcoming if str(p["ProjectNumber"]) not in previous_state["upcoming"]]

    for p in new_open:
        p["ProjectStatus"] = 4
    for p in new_upcoming:
        p["ProjectStatus"] = 2

    if new_open or new_upcoming:
        message = "🆕 *פרויקטים חדשים:*\n"
        for p in new_open:
            message += f"🏠 *{p['ProjectName']}* ({p['CityDescription']}) – פתוח\n"
        for p in new_upcoming:
            message += f"📅 *{p['ProjectName']}* ({p['CityDescription']}) – טרם נפתח\n"

        send_telegram(CHANNEL_ID, message)
        send_telegram(PERSONAL_ID, "📣 נשלחה הודעה לקבוצה – יש פרויקטים חדשים.")
        write_projects_to_csv(new_open + new_upcoming)
    else:
        send_telegram(PERSONAL_ID, "✅ אין פרויקטים חדשים היום. הסקריפט רץ כרגיל.")

    save_state(current_state)

if __name__ == "__main__":
    check_new_projects()