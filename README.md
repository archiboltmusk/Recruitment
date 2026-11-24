# MedAlerts - All India Medical Officer Vacancies Aggregator & Notifier

**MedAlerts** is an open-source recruitment aggregation and notification engine specifically built for Medical Officers (MOs), General Duty Medical Officers (GDMOs), Assistant Divisional Medical Officers (ADMOs), Specialists, and AYUSH doctors across India.

It solves the problem of doctor recruitment notifications being scattered across hundreds of separate central portals, State Public Service Commissions, National Health Mission (NHM) directorates, and AIIMS institutes.

---

## 🌟 Key Features

1. **Centralized Directory**: Consolidates posts from:
   - **Central Government:** UPSC (Combined Medical Services / CMS), ESIC (IMO Gr-II), Indian Railways, AFMS (Army/Navy/Air Force Medical Services).
   - **Autonomous Institutes:** AIIMS (New Delhi & regional AIIMS), PGIMER, JIPMER.
   - **State PSCs:** UPPSC, MPSC, TN MRB, BPSC, KPSC, etc.
   - **NHM / Contractual:** High-volume state and district health society posts.
   - **AYUSH & Dental:** BAMS, BHMS, and BDS openings.
2. **Instant Multi-Channel Alerts**:
   - **Telegram Channel / Bot:** Broadcasts formatted HTML job alerts with direct PDF links.
   - **Email / Webhook Integrations:** Supports automated subscriber digests.
3. **Smart Filters & Deadlines**:
   - Filter by stream (`MBBS`, `MD/MS Specialist`, `AYUSH`, `BDS`).
   - Filter by cadre (`Central Govt`, `State PSC`, `NHM`).
   - Countdown tracker highlighting vacancies closing in `< 7 days`.
4. **Interactive Dashboard**:
   - Responsive web UI built with Tailwind CSS, real-time sync, and subscription modal.

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.9+
- SQLite (default) or PostgreSQL

### 2. Setup & Installation
```bash
cd /Users/anupam/.gemini/antigravity/scratch/medical-officer-alerts

# Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start the Server
```bash
./venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Open your browser to:
- **Web App Dashboard:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📲 Setting up Live Telegram Notifications

1. Open Telegram and message [@BotFather](https://t.me/BotFather) to create a new bot (e.g. `MedAlertsBot`).
2. Copy the **HTTP API Token** provided by BotFather.
3. Export the environment variable before starting the app:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_bot_token_here"
   ./venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```
4. Whenever a new vacancy is synced or published, any subscriber with a valid Telegram Chat ID or public channel (`@channel_name`) will receive real-time push alerts.

---

## 📂 Project Architecture

```
medical-officer-alerts/
├── app/
│   ├── database.py       # Database connection & SQLAlchemy setup
│   ├── models.py         # Schema for Vacancies, Subscriptions, and NotificationLogs
│   ├── collector.py      # Aggregator, feed parser & sample data sync
│   ├── notifier.py       # Telegram, Email & Webhook dispatch engine
│   ├── main.py           # FastAPI application endpoints
│   └── static/
│       └── index.html    # Modern interactive responsive dashboard
├── requirements.txt      # Python dependencies
└── README.md             # Documentation
```

---

## 🔌 Adding Real-Time Web Scrapers

In `app/collector.py`, you can attach automated daily scrapers for target portals using `BeautifulSoup` or `playwright`:
```python
import requests
from bs4 import BeautifulSoup

def scrape_upsc_notices():
    url = "https://upsc.gov.in/examinations/active-examinations"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")
    # Search for keywords: "Combined Medical Services", "Medical Officer"
    # Extract notification PDF link and deadline
```
Then schedule via cron or Celery/APScheduler.
