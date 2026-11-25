import json
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from .models import Vacancy
from .notifier import Notifier
from .pdf_parser import GovtNotificationPDFParser

logger = logging.getLogger("medalerts.scraper")

MEDICAL_PATTERN = re.compile(
    r"\b(medical officer|gdmo|cms|combined medical|imo|insurance medical|senior resident|sr\.?\s*resident|junior resident|jr\.?\s*resident|rmo|rmo-cum-tutor|clinical tutor|demonstrator|specialist|part-time specialist|super specialist|house staff|house staffship|house-staff|ptmo|health officer|doctor|ayush|nuhm|uhwc|walk-in|contract medical|cmp)\b",
    re.IGNORECASE,
)

NON_JOB_PATTERN = re.compile(
    r"\b(merit\s*list|selected\s*(?:candidate|list)|shortlisted|waiting\s*list|waitlist|result(?:s)?\s+(?:of|for)|admit\s*card|corrigendum|addendum|cancellation|cancelled|answer\s*key|provisional\s*list|final\s*list|joining\s*order|panel\s*for|engagement\s*order)\b",
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
    {
        "name": "Purulia_CMOH",
        "organization": "Purulia District Health & Family Welfare Samiti (CMOH)",
        "url": "https://purulia.gov.in/past-notices/recruitment/",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated NHM / FRU GDMO)",
    },
    {
        "name": "NRS_Kolkata",
        "organization": "Nil Ratan Sircar Medical College & Hospital (NRSMC), Kolkata",
        "url": "https://nrsmc.edu.in/",
        "category": "WB Medical College (JR / House Staff / RMO)",
        "state": "West Bengal",
        "pay_scale": "WB Govt House Staff / JR Stipend / RMO Pay",
    },
    # --- Defence, Paramilitary, Railways & Central PSUs ---
    {
        "name": "AFMS_SSC",
        "organization": "Armed Forces Medical Services (AFMS SSC Medical Officer)",
        "url": "https://join.afms.gov.in/",
        "category": "Defence / Central Govt",
        "state": "All India",
        "pay_scale": "Level 10B (Captain Rank) + MSP ₹15,500 + 20% NPA",
    },
    {
        "name": "CAPF_ITBP",
        "organization": "CAPF Medical Officer Selection Board (ITBP / CRPF / BSF / SSB)",
        "url": "https://recruitment.itbpolice.nic.in/",
        "category": "CAPF / Central Govt",
        "state": "All India",
        "pay_scale": "Level 10 (Assistant Commandant MO ₹56,100) + 20% NPA",
    },
    {
        "name": "SAIL_Careers",
        "organization": "Steel Authority of India Limited (SAIL — Burnpur / Durgapur / Bokaro)",
        "url": "https://sailcareers.com/",
        "category": "Central Govt / PSU",
        "state": "All India",
        "pay_scale": "E-1 / E-3 Medical Executive Scale or Walk-in GDMO",
    },
    {
        "name": "Coal_India",
        "organization": "Coal India Limited (CIL / ECL / BCCL Medical Executive)",
        "url": "https://www.coalindia.in/career-cil/jobs-coal-india/",
        "category": "Central Govt / PSU",
        "state": "All India",
        "pay_scale": "E-3 Medical Executive (₹60,000 - ₹1,80,000) + NPA",
    },
    # --- National Institutes (INIs) & Central Govt Hospitals (JR / SR / MO) ---
    {
        "name": "PGIMER_Chandigarh",
        "organization": "PGIMER, Chandigarh",
        "url": "https://pgimer.edu.in/PGIMER_PORTAL/PGIMERPORTAL/Vacancies/JSP/VACANCIE_VIEW.jsp?countt=0",
        "category": "Autonomous Institute",
        "state": "Chandigarh",
        "pay_scale": "Level 10 (SMO / Demonstrator) / Level 11 (SR) + NPA",
    },
    {
        "name": "JIPMER_Puducherry",
        "organization": "JIPMER, Puducherry",
        "url": "https://jipmer.edu.in/announcement/jobs",
        "category": "Autonomous Institute",
        "state": "Puducherry",
        "pay_scale": "Level 10 (JR ₹56,100+NPA) / Level 11 (SR ₹67,700+NPA)",
    },
    {
        "name": "AIIMS_Deoghar",
        "organization": "AIIMS Deoghar (Jharkhand)",
        "url": "https://www.aiimsdeoghar.edu.in/recruitments/list",
        "category": "Autonomous Institute",
        "state": "Jharkhand",
        "pay_scale": "Level 10 (JR) / Level 11 (SR ₹67,700+NPA)",
    },
    {
        "name": "VMMC_Safdarjung",
        "organization": "VMMC & Safdarjung Hospital, New Delhi",
        "url": "https://vmmc-sjh.mohfw.gov.in/",
        "category": "Central Govt",
        "state": "Delhi",
        "pay_scale": "Level 10 (Non-PG JR ₹56,100+NPA) / Level 11 (SR)",
    },
    {
        "name": "ABVIMS_RMLH",
        "organization": "ABVIMS & Dr. Ram Manohar Lohia Hospital, New Delhi",
        "url": "https://rmlh.mohfw.gov.in/index1.aspx?lsid=201&lev=2&lid=181&langid=1",
        "category": "Central Govt",
        "state": "Delhi",
        "pay_scale": "Level 10 (Non-PG JR ₹56,100+NPA) / Level 11 (SR)",
    },
    {
        "name": "Delhi_Health_HFW",
        "organization": "Delhi Health & Family Welfare (GIPMER / LNH / JPCH / GGSGH)",
        "url": "https://health.delhi.gov.in/vacancy",
        "category": "State Govt / JR Walk-in",
        "state": "Delhi",
        "pay_scale": "Level 10 (₹56,100 - ₹1,77,500) + NPA & Allowances",
    },
    {
        "name": "BHEL_Careers",
        "organization": "Bharat Heavy Electricals Limited (BHEL — GDMO & PTMC)",
        "url": "https://careers.bhel.in/",
        "category": "Central Govt / PSU",
        "state": "All India",
        "pay_scale": "E-1 / E-2 Medical Executive Scale or ₹500/hr PTMC",
    },
    {
        "name": "BEL_Careers",
        "organization": "Bharat Electronics Limited (BEL — Medical Officer E-II)",
        "url": "https://bel-india.in/job-notifications/",
        "category": "Central Govt / PSU",
        "state": "All India",
        "pay_scale": "E-II Grade (₹40,000 - ₹1,40,000) + DA/Perks",
    },
    {
        "name": "Tata_Memorial_TMC",
        "organization": "Tata Memorial Centre (TMC — Mumbai / Homi Bhabha)",
        "url": "https://tmc.gov.in/postmaster/Careers",
        "category": "Autonomous Institute",
        "state": "Maharashtra",
        "pay_scale": "Level 10 / Level 11 (MO / SR) + Allowances",
    },
    {
        "name": "ISRO_Careers",
        "organization": "Indian Space Research Organisation (ISRO — Medical Officer SD)",
        "url": "https://www.isro.gov.in/Careers.html",
        "category": "Central Govt",
        "state": "All India",
        "pay_scale": "Level 11 (Medical Officer 'SD') + NPA & Perks",
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
        if re.search(r"\b(?:senior\s+resident|sr\.?\s*resident|specialist)\b", low):
            return {"qualification": "MD/MS", "designation": "Senior Resident / Specialist"}
        if "rmo" in low or "clinical tutor" in low:
            return {"qualification": "MBBS / MD/MS", "designation": "RMO-cum-Clinical Tutor"}
        if re.search(r"\b(?:junior\s+resident|jr\.?\s*resident|house[-\s]?staff)\b", low):
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
            if not MEDICAL_PATTERN.search(post_name) or NON_JOB_PATTERN.search(row_text):
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
                "total_posts": 0,
                "pay_scale": source["pay_scale"],
                "last_date": last_date,
                "notification_url": source["url"],
                "apply_url": source["url"],
                "summary": f"Live WB Health district online recruitment ({programme}). {schedule_text[:180]}",
                "selection_mode": "Online Merit / Interview (hr.wbhealth.gov.in)",
                "bond_years": 0,
                "bond_penalty_amount": "No Bond (Contractual)",
                "verification_status": "PORTAL_VERIFIED" if last_date else "NEEDS_PDF_CHECK",
            })
            if len(discovered) >= 12:
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
            pdf_parsed_count = 0
            for a in soup.find_all("a", href=True):
                text = " ".join(a.get_text(" ", strip=True).split())
                if len(text) < 12:
                    parent_row = a.find_parent("tr")
                    if parent_row:
                        text = " ".join(parent_row.get_text(" ", strip=True).split())
                if len(text) < 12 or len(text) > 260:
                    continue
                low = text.lower()
                if not MEDICAL_PATTERN.search(text) or NON_JOB_PATTERN.search(text):
                    continue
                if text in seen_titles:
                    continue
                seen_titles.add(text)

                full_url = urljoin(source["url"], a["href"])
                is_walkin = "walk-in" in low or "walk in" in low or "contract" in low
                role_info = cls._infer_role_and_qual(text)

                entry: Dict[str, Any] = {
                    "title": text[:250],
                    "organization": source["organization"],
                    "category": "Contractual / Walk-in" if is_walkin else source["category"],
                    "state": source["state"],
                    "designation": role_info["designation"],
                    "qualification": role_info["qualification"],
                    "total_posts": 0,
                    "pay_scale": source["pay_scale"],
                    "last_date": None,
                    "exam_date": None,
                    "notification_url": full_url,
                    "apply_url": source["url"],
                    "summary": f"Live circular discovered from {source['organization']}. Open the official PDF to verify exact seat count and deadline.",
                    "selection_mode": "Walk-in Interview" if is_walkin else "Written Exam / Interview",
                    "bond_years": 0,
                    "bond_penalty_amount": "Check Official Notice",
                    "verification_status": "NEEDS_PDF_CHECK",
                }

                if ".pdf" in full_url.lower() and pdf_parsed_count < 6:
                    pdf_parsed_count += 1
                    try:
                        pdf_text = GovtNotificationPDFParser.extract_from_url(full_url)
                        parsed = GovtNotificationPDFParser.parse_notice_text(pdf_text)
                        if parsed.get("total_posts"):
                            entry["total_posts"] = parsed["total_posts"]
                        if parsed.get("pay_scale"):
                            entry["pay_scale"] = parsed["pay_scale"]
                        if parsed.get("min_age"):
                            entry["min_age"] = parsed["min_age"]
                        if parsed.get("max_age"):
                            entry["max_age"] = parsed["max_age"]
                        if parsed.get("last_date"):
                            entry["last_date"] = datetime.strptime(parsed["last_date"], "%Y-%m-%d")
                        if parsed.get("exam_date"):
                            entry["exam_date"] = datetime.strptime(parsed["exam_date"], "%Y-%m-%d")
                        if parsed.get("selection_mode"):
                            entry["selection_mode"] = parsed["selection_mode"]
                        if parsed.get("bond_years"):
                            entry["bond_years"] = parsed["bond_years"]
                            entry["bond_penalty_amount"] = parsed["bond_penalty_amount"]
                        if parsed.get("category_seats"):
                            entry["category_seats_json"] = json.dumps(parsed["category_seats"])
                        if parsed.get("application_fee"):
                            entry["application_fee"] = parsed["application_fee"]
                        if parsed.get("memo_number"):
                            entry["memo_number"] = parsed["memo_number"]
                        if parsed.get("parsed_confident"):
                            entry["verification_status"] = "VERIFIED_PDF"
                            entry["summary"] = f"Auto-parsed from official PDF ({parsed.get('memo_number') or source['name']}). Verify annexures before applying."
                    except Exception as pdf_err:
                        logger.debug(f"PDF auto-parse skipped for {full_url}: {pdf_err}")

                today = datetime.utcnow().date()
                if entry.get("last_date") and entry["last_date"].date() < today:
                    continue
                if not entry.get("last_date") and entry.get("exam_date") and entry["exam_date"].date() < today:
                    continue

                discovered.append(entry)
                if len(discovered) >= 12:
                    break
        except Exception as e:
            logger.warning(f"Live scrape skipped for {source['name']}: {e}")
        return discovered

    @classmethod
    def sync_live_portals(cls, db: Session) -> Dict[str, Any]:
        added = 0
        checked_portals = 0
        now = datetime.utcnow()
        db.query(Vacancy).filter(
            Vacancy.is_active == True,
            Vacancy.last_date.isnot(None),
            Vacancy.last_date < now,
        ).update({"is_active": False, "stage": "APPLICATION_CLOSED"}, synchronize_session=False)
        db.query(Vacancy).filter(
            Vacancy.is_active == True,
            Vacancy.last_date.is_(None),
            Vacancy.verification_status == "NEEDS_PDF_CHECK",
            Vacancy.created_at < now - timedelta(days=30),
        ).update({"is_active": False, "stage": "APPLICATION_CLOSED"}, synchronize_session=False)
        db.commit()

        all_discovered: List[Dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(cls.fetch_portal_links, src): src for src in PORTAL_SOURCES}
            for fut in as_completed(futures):
                checked_portals += 1
                src = futures[fut]
                try:
                    for item in fut.result():
                        all_discovered.append((src["url"], item))
                except Exception as exc:
                    logger.warning(f"Concurrent fetch failed for {src['name']}: {exc}")

        for portal_root_url, item in all_discovered:
            existing = db.query(Vacancy).filter(
                Vacancy.title == item["title"],
                Vacancy.organization == item["organization"],
            ).first()
            if not existing and item.get("notification_url") and item["notification_url"] != portal_root_url:
                existing = db.query(Vacancy).filter(
                    Vacancy.notification_url == item["notification_url"]
                ).first()
            if not existing and item.get("memo_number"):
                existing = db.query(Vacancy).filter(
                    Vacancy.memo_number == item["memo_number"]
                ).first()
            if not existing:
                v = Vacancy(**item, stage="APPLICATION_OPEN", is_active=True)
                db.add(v)
                db.commit()
                db.refresh(v)
                Notifier.broadcast_new_vacancy(db, v)
                added += 1
        return {"portals_checked": checked_portals, "live_added": added}
