import csv
from pathlib import Path
from datetime import datetime

CSV_PATH = Path("new_projects.csv")

def write_projects_to_csv(projects: list[dict]):
    is_new = not CSV_PATH.exists()
    with open(CSV_PATH, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["date", "project_number", "project_name", "city", "status"])
        for p in projects:
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d"),
                p["ProjectNumber"],
                p["ProjectName"],
                p["CityDescription"],
                "פתוח" if p["ProjectStatus"] == 4 else "טרם נפתח"
            ])