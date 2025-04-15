import requests
import json
from pathlib import Path
from urllib.parse import quote

BASE_URL = "https://www.dira.moch.gov.il/api/Invoker"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.dira.moch.gov.il/ProjectsList"
}

STATE_PATH = Path("state.json")

def fetch_projects(status: int) -> list[dict]:
    """Fetch projects by ProjectStatus (2=upcoming, 4=open)"""
    raw_param = f"?ProjectStatus={status}&Entitlement=1&PageNumber=1&PageSize=50&IsInit=false"
    encoded_param = quote(raw_param, safe="")
    url = f"{BASE_URL}?method=Projects&param={encoded_param}"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json().get("ProjectItems", [])

def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"open": [], "upcoming": []}

def save_state(state: dict):
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False))

def extract_ids(projects: list[dict]) -> list[str]:
    return [str(p["ProjectNumber"]) for p in projects]

def check_new_projects():
    current_open = fetch_projects(4)
    current_upcoming = fetch_projects(2)

    current_state = {
        "open": extract_ids(current_open),
        "upcoming": extract_ids(current_upcoming),
    }

    previous_state = load_state()

    new_open = [p for p in current_open if str(p["ProjectNumber"]) not in previous_state["open"]]
    new_upcoming = [p for p in current_upcoming if str(p["ProjectNumber"]) not in previous_state["upcoming"]]

    if new_open:
        print("🔔 New projects open for registration:")
        for p in new_open:
            print(f"- {p['ProjectName']} | {p['CityDescription']} | #{p['ProjectNumber']}")
    if new_upcoming:
        print("🔔 New upcoming projects (not open yet):")
        for p in new_upcoming:
            print(f"- {p['ProjectName']} | {p['CityDescription']} | #{p['ProjectNumber']}")
    if not new_open and not new_upcoming:
        print("✅ No new projects.")

    save_state(current_state)

if __name__ == "__main__":
    check_new_projects()