import logging
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from .models import Vacancy
from .notifier import Notifier

logger = logging.getLogger("medalerts.scraper")

MEDICAL_PATTERN = re.compile(
    r"\b(medical officer|gdmo|cms|combined medical|imo|insurance medical|senior resident|junior resident|rmo|rmo-cum-tutor|clinical tutor|demonstrator|specialist|part-time specialist|super specialist|house staff|house staffship|house-staff|ptmo|health officer|doctor|ayush|nuhm|uhwc|walk-in|contract medical|cmp)\b",
    re.IGNORECASE,
)

WBHEALTH_HR_REG_DATE_RE = re.compile(
    r"Last Date for Registration is\s+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
    re.IGNORECASE,
)

PORTAL_SOURCES = [
    # --- Central & All-India Portals ---
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
        "organization": "Employees' State Insurance Corporation (ESIC / Joka & All-India)",
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
    # --- West Bengal State Health & Statutory Boards ---
    {
        "name": "WBHRB",
        "organization": "West Bengal Health Recruitment Board (WBHRB)",
        "url": "https://www.hrb.wb.gov.in/notice",
        "category": "State PSC / WBHRB",
        "state": "West Bengal",
        "pay_scale": "Pay Level 16 (WBHS ₹56,100 - ₹1,44,300) + NPA",
    },
    {
        "name": "WBHealth",
        "organization": "WB State Health & Family Welfare Samiti (Swasthya Bhawan)",
        "url": "https://www.wbhealth.gov.in/pages/career",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated NUHM / NHM)",
    },
    {
        "name": "WBHealth_HR",
        "organization": "WB Health District CMOH / DH&FWS Online Portal",
        "url": "https://hr.wbhealth.gov.in/Index.aspx",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated NHM / NUHM / FRU)",
        "parser": "wbhealth_hr_table",
    },
    {
        "name": "ESI_WB",
        "organization": "Directorate of ESI (MB) Scheme, West Bengal",
        "url": "https://esiwb.gov.in/home/employment_notice",
        "category": "ESIC / State Govt",
        "state": "West Bengal",
        "pay_scale": "WB ROPA Level 16 / Walk-in Consolidated",
    },
    # --- West Bengal Municipalities & Urban Local Bodies ---
    {
        "name": "WBMSC",
        "organization": "West Bengal Municipal Service Commission (WBMSC)",
        "url": "https://mscwb.org/home/emp_notice",
        "category": "State PSC / Municipality",
        "state": "West Bengal",
        "pay_scale": "WB ROPA Level 16 (KMC / ULB Permanent MO)",
    },
    {
        "name": "KMC_Kolkata",
        "organization": "Kolkata Municipal Corporation (KMC Health / NUHM)",
        "url": "https://www.kmcgov.in/KMCPortal/jsp/Recruitment2015.jsp",
        "category": "Contractual / Walk-in",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Full-Time) | ₹24,000/month (PTMO)",
    },
    {
        "name": "SUDA_WB",
        "organization": "State Urban Development Agency (SUDA), West Bengal",
        "url": "https://sudawb.org/Emp-Notice",
        "category": "Municipality / ULB",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated ULB Health Officer / MO)",
    },
    {
        "name": "Siliguri_SMC",
        "organization": "Siliguri Municipal Corporation (SMC)",
        "url": "https://www.siligurismc.in/recruitments.php",
        "category": "Contractual / Walk-in",
        "state": "West Bengal",
        "pay_scale": "₹24,000 - ₹60,000/month (PTMO / NUHM MO)",
    },
    {
        "name": "Howrah_HMC",
        "organization": "Howrah Municipal Corporation (HMC Health / NUHM)",
        "url": "https://www.myhmc.in/health-officer/",
        "category": "Contractual / Walk-in",
        "state": "West Bengal",
        "pay_scale": "₹24,000 - ₹60,000/month (PTMO / NUHM MO)",
    },
    # --- West Bengal Medical Colleges & Autonomous Hospitals (JR / House Staff / RMO) ---
    {
        "name": "AIIMS_Kalyani",
        "organization": "AIIMS Kalyani (West Bengal)",
        "url": "https://aiimskalyani.edu.in/recruitment",
        "category": "Autonomous Institute",
        "state": "West Bengal",
        "pay_scale": "Level 10 (JR ₹56,100+NPA) / Level 11 (SR ₹67,700+NPA)",
    },
    {
        "name": "IPGMER_SSKM",
        "organization": "IPGMER & SSKM Hospital, Kolkata",
        "url": "https://ipgmer.gov.in/notice_tender",
        "category": "WB Medical College (JR / House Staff / RMO)",
        "state": "West Bengal",
        "pay_scale": "WB Govt House Staff / JR Stipend / RMO Pay",
    },
    {
        "name": "MCH_Kolkata",
        "organization": "Medical College & Hospital, Kolkata (MCH)",
        "url": "https://www.medicalcollegekolkata.in/main/page/Recruitment_Notice958d34",
        "category": "WB Medical College (JR / House Staff / RMO)",
        "state": "West Bengal",
        "pay_scale": "WB Govt House Staff / JR / RMO Scale",
    },
    {
        "name": "CNMC_Kolkata",
        "organization": "Calcutta National Medical College & Hospital (CNMC), Kolkata",
        "url": "https://www.cnmckolkata.com/notice.php",
        "category": "WB Medical College (JR / House Staff / RMO)",
        "state": "West Bengal",
        "pay_scale": "WB Govt House Staff / JR Stipend",
    },
    {
        "name": "CNCI_Kolkata",
        "organization": "Chittaranjan National Cancer Institute (CNCI), Kolkata",
        "url": "https://cnci.ac.in/doctors-faculties-positions-1",
        "category": "Autonomous Institute",
        "state": "West Bengal",
        "pay_scale": "Level 10 (JR / MO) / Level 11 (SR) + NPA",
    },
    # --- West Bengal Port / PSU & District Portals ---
    {
        "name": "SMPK_Kolkata",
        "organization": "Syama Prasad Mookerjee Port, Kolkata (Centenary Hospital)",
        "url": "https://smportkolkata.shipping.gov.in/smpk/en/job-openings/",
        "category": "Central Govt / PSU",
        "state": "West Bengal",
        "pay_scale": "Port Class-I Medical Officer Scale / Contractual",
    },
    {
        "name": "Purba_Bardhaman_CMOH",
        "organization": "Purba Bardhaman District & Burdwan Medical College",
        "url": "https://www.purbabardhaman.gov.in/notice_category/recruitment/",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (NHM MO) / WB SR Scale",
    },
    {
        "name": "Bankura_CMOH",
        "organization": "Bankura District Health & Family Welfare Samiti (CMOH)",
        "url": "https://bankura.gov.in/past-notices/recruitment/",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated NHM / FRU GDMO)",
    },
]


class LiveGazetteScraper:
    """Safely polls official Indian & West Bengal recruitment portals for GDMO, JR, and RMO notices."""

    HEADERS = {
        "User-Agent": "MedAlertsBot/2.0 (+https://medalerts.onrender.com; medical-recruitment-aggregator)"
    }

    @staticmethod
    def _infer_role_and_qual(text: str) -> Dict[str, str]:
        low = text.lower()
        if "ayush" in low or "ayurved" in low or "homeopath" in low:
            return {"qualification": "AYUSH", "designation": "AYUSH Medical Officer"}
        if "senior resident" in low or "specialist" in low:
            return {"qualification": "MD/MS", "designation": "Senior Resident / Specialist"}
        if "rmo" in low or "clinical tutor" in low:
            return {"qualification": "MBBS / MD/MS", "designation": "RMO-cum-Clinical Tutor"}
        if "junior resident" in low or "house staff" in low or "house-staff" in low:
            return {"qualification": "MBBS", "designation": "Junior Resident / House Staff"}
        return {"qualification": "MBBS", "designation": "Medical Officer / GDMO"}

    @staticmethod
    def _parse_wbhealth_hr_table(soup: BeautifulSoup, source: Dict[str, str]) -> List[Dict[str, Any]]:
        """Parses the live district recruitment table on hr.wbhealth.gov.in/Index.aspx with exact deadlines."""
        discovered: List[Dict[str, Any]] = []
        seen = set()
        now = datetime.utcnow()

        for tr in soup.find_all("tr"):
            cells = [" ".join(td.get_text(" ", strip=True).split()) for td in tr.find_all("td")]
            if len(cells) < 3:
                continue
            post_name, programme, schedule_text = cells[0], cells[1], cells[2]
            row_text = " ".join(cells)
            if "Continue For Registration" not in row_text:
                continue
            if not MEDICAL_PATTERN.search(post_name):
                continue

            title = f"{post_name} ({programme})"[:250]
            if title in seen:
                continue
            seen.add(title)

            last_date: Optional[datetime] = None
            m = WBHEALTH_HR_REG_DATE_RE.search(schedule_text)
            if m:
                try:
                    last_date = datetime.strptime(m.group(1), "%d %b %Y")
                except ValueError:
                    last_date = None
            if last_date and last_date.date() < now.date():
                continue

            role_info = LiveGazetteScraper._infer_role_and_qual(post_name)
            discovered.append({
                "title": title,
                "organization": f"CMOH / DH&FWS — {programme}"[:250],
                "category": source["category"],
                "state": source["state"],
                "designation": role_info["designation"],
                "qualification": role_info["qualification"],
                "total_posts": 1,
                "pay_scale": source["pay_scale"],
                "last_date": last_date or (now + timedelta(days=14)),
                "notification_url": source["url"],
                "apply_url": source["url"],
                "summary": f"Live WB Health district online recruitment ({programme}). {schedule_text[:180]}",
                "selection_mode": "Online Merit / Interview (hr.wbhealth.gov.in)",
                "bond_years": 0,
                "bond_penalty_amount": "No Bond (Contractual)",
            })
            if len(discovered) >= 10:
                break
        return discovered

    @classmethod
    def fetch_portal_links(cls, source: Dict[str, str]) -> List[Dict[str, Any]]:
        discovered: List[Dict[str, Any]] = []
        try:
            resp = requests.get(source["url"], headers=cls.HEADERS, timeout=8)
            if not resp.ok:
                logger.warning(f"Portal {source['name']} returned HTTP {resp.status_code}")
                return discovered

            soup = BeautifulSoup(resp.text, "html.parser")
            if source.get("parser") == "wbhealth_hr_table":
                return cls._parse_wbhealth_hr_table(soup, source)

            seen_titles = set()
            for a in soup.find_all("a", href=True):
                text = " ".join(a.get_text(" ", strip=True).split())
                if len(text) < 12:
                    parent_row = a.find_parent("tr")
                    if parent_row:
                        text = " ".join(parent_row.get_text(" ", strip=True).split())
                if len(text) < 12 or len(text) > 260:
                    continue
                low = text.lower()
                if not MEDICAL_PATTERN.search(text):
                    continue
                if text in seen_titles:
                    continue
                seen_titles.add(text)

                full_url = urljoin(source["url"], a["href"])
                is_walkin = "walk-in" in low or "walk in" in low or "contract" in low
                role_info = cls._infer_role_and_qual(text)
                discovered.append({
                    "title": text[:250],
                    "organization": source["organization"],
                    "category": "Contractual / Walk-in" if is_walkin else source["category"],
                    "state": source["state"],
                    "designation": role_info["designation"],
                    "qualification": role_info["qualification"],
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
