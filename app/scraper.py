import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from .models import Vacancy
from .notifier import Notifier

logger = logging.getLogger("medalerts.scraper")

MEDICAL_KEYWORDS = (
    "medical officer", "gdmo", "cms", "combined medical", "imo",
    "senior resident", "junior resident", "specialist", "doctor",
    "ayush", "walk-in", "contract medical", "cmp"
)

PORTAL_SOURCES = [
    {
        "name": "UPSC",
        "organization": "Union Public Service Commission (UPSC)",
        "url": "https://upsc.gov.in/whats-new",
        "category": "Central Govt",
        "state": "All India",
        "pay_scale": "Level 10 (₹56,100 - ₹1,77,500) + 20% NPA",
    },
    {
        "name": "ESIC",
        "organization": "Employees' State Insurance Corporation (ESIC)",
        "url": "https://www.esic.gov.in/recruitments",
        "category": "ESIC / Central Govt",
        "state": "All India",
        "pay_scale": "Level 10 / Walk-in Consolidated",
    },
    {
        "name": "AIIMS",
        "organization": "AIIMS Examinations Section",
        "url": "https://www.aiimsexams.ac.in/info/Recruitments.html",
        "category": "Autonomous Institute",
        "state": "Delhi / Multi-State",
        "pay_scale": "Level 10 / Level 11 + NPA",
    },
]


class LiveGazetteScraper:
    """Safely polls official Indian government recruitment portals for new Medical Officer notices."""

    HEADERS = {
        "User-Agent": "MedAlertsBot/2.0 (+https://medalerts.onrender.com; medical-recruitment-aggregator)"
    }

    @classmethod
    def fetch_portal_links(cls, source: Dict[str, str]) -> List[Dict[str, Any]]:
        discovered: List[Dict[str, Any]] = []
        try:
            resp = requests.get(source["url"], headers=cls.HEADERS, timeout=8)
            if not resp.ok:
                logger.warning(f"Portal {source['name']} returned HTTP {resp.status_code}")
                return discovered

            soup = BeautifulSoup(resp.text, "html.parser")
            seen_titles = set()
            for a in soup.find_all("a", href=True):
                text = " ".join(a.get_text(" ", strip=True).split())
                if len(text) < 12 or len(text) > 220:
                    continue
                low = text.lower()
                if not any(kw in low for kw in MEDICAL_KEYWORDS):
                    continue
                if text in seen_titles:
                    continue
                seen_titles.add(text)

                full_url = urljoin(source["url"], a["href"])
                is_walkin = "walk-in" in low or "walk in" in low or "contract" in low
                qual = "MD/MS" if ("senior resident" in low or "specialist" in low) else (
                    "AYUSH" if "ayush" in low else "MBBS"
                )
                discovered.append({
                    "title": text[:250],
                    "organization": source["organization"],
                    "category": "Contractual / Walk-in" if is_walkin else source["category"],
                    "state": source["state"],
                    "designation": "Senior Resident / Specialist" if qual == "MD/MS" else "Medical Officer / GDMO",
                    "qualification": qual,
                    "total_posts": 10,
                    "pay_scale": source["pay_scale"],
                    "last_date": datetime.utcnow() + timedelta(days=14),
                    "notification_url": full_url,
                    "apply_url": source["url"],
                    "summary": f"Live circular discovered from {source['organization']}. Verify official PDF for exact vacancy count and deadline.",
                    "selection_mode": "Walk-in Interview" if is_walkin else "Written Exam / Interview",
                    "bond_years": 0,
                    "bond_penalty_amount": "Check Official Notice",
                })
                if len(discovered) >= 5:
                    break
        except Exception as e:
            logger.warning(f"Live scrape skipped for {source['name']}: {e}")
        return discovered

    @classmethod
    def sync_live_portals(cls, db: Session) -> Dict[str, Any]:
        added = 0
        checked_portals = 0
        for source in PORTAL_SOURCES:
            checked_portals += 1
            items = cls.fetch_portal_links(source)
            for item in items:
                existing = db.query(Vacancy).filter(
                    Vacancy.title == item["title"],
                    Vacancy.organization == item["organization"]
                ).first()
                if not existing:
                    v = Vacancy(**item, stage="APPLICATION_OPEN", is_active=True)
                    db.add(v)
                    db.commit()
                    db.refresh(v)
                    Notifier.broadcast_new_vacancy(db, v)
                    added += 1
        return {"portals_checked": checked_portals, "live_added": added}
