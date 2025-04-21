
# 📦 Dira Watcher – ניטור פרויקטים חדשים באתר דירה בהנחה

![GitHub Workflow Status](https://github.com/orguetta/Dira/actions/workflows/check-dira.yml/badge.svg)

[![Join the Telegram Channel](https://img.shields.io/badge/Telegram-Join%20Channel-blue?logo=telegram)](https://t.me/dira_beanha)

מערכת ב־Python שבודקת מדי יום אם נוספו פרויקטים חדשים באתר [דירה בהנחה](https://www.dira.moch.gov.il/ProjectsList), שולחת עדכון לטלגרם, ושומרת את המידע ל־CSV לצורך תיעוד.

## ✨ פיצ'רים

- ✅ בדיקה יומית מול ממשק ה־API הסמוי של האתר
- ✅ תמיכה בפרויקטים *פתוחים להרשמה* ו־*טרם נפתחו להרשמה*
- ✅ שליחת הודעה לקבוצת טלגרם במקרה של עדכון
- ✅ שליחת heartbeat אישי במקרה ואין שינוי (לוודא שהסקריפט רץ)
- ✅ שמירת הפרויקטים החדשים ל־`new_projects.csv`
- ✅ שמירת מצב קודם ב־`state.json` למניעת התראות חוזרות
- ✅ אוטומציה מלאה ב־GitHub Actions עם `uv`

## 📁 מבנה הפרויקט

```
.
├── scripts/
│   ├── check_dira.py      # הסקריפט הראשי
│   ├── telegram.py        # שליחה לטלגרם עם MarkdownV2 ותמיכה בחיתוך
│   └── csv_writer.py      # כתיבה ל־CSV
├── new_projects.csv       # מתעדכן אוטומטית
├── state.json             # שומר את מזהי הפרויקטים שנסרקו בעבר
├── pyproject.toml         # ניהול תלויות עם uv
└── .github/workflows/
    └── check-dira.yml     # הרצת הסקריפט אוטומטית פעם ביום
```

## ⚙️ הגדרת משתנים סודיים (GitHub Secrets)

יש להוסיף את הסודות הבאים בריפוזיטורי תחת:  
`Settings > Secrets and variables > Actions`

| שם                  | הסבר |
|----------------------|------|
| `TELEGRAM_BOT_TOKEN` | הטוקן של הבוט שלך |
| `TELEGRAM_CHANNEL_ID` | ID של הקבוצה / ערוץ (למשל `@my_channel` או `-1001234567890`) |
| `TELEGRAM_PERSONAL_ID` | ה־chat ID שלך לצורך הודעות אישיות |

## 🚀 הפעלה מקומית

```bash
uv venv
uv pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN=...
export TELEGRAM_CHANNEL_ID=...
export TELEGRAM_PERSONAL_ID=...
uv run scripts/check_dira.py
```

## 🧠 הערות

- הקובץ `state.json` נשמר בגיט כדי לשמר מצב בין הרצות (מומלץ לעדכן אותו עם כל commit אוטומטי).
- הקובץ `new_projects.csv` מתעדכן רק כאשר נמצאו פרויקטים חדשים.
- כל הודעה שעוברת את 4096 תווים תיחתך אוטומטית ונשלח במספר הודעות.
- אם יש צורך להפסיק את ההודעות האישיות, ניתן להגדיר את `TELEGRAM_PERSONAL_ID` ל־`None`.
- אם יש צורך להפסיק את ההודעות לקבוצת טלגרם, ניתן להגדיר את `TELEGRAM_CHANNEL_ID` ל־`None`.

