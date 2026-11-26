import json
import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import urljoin
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from .models import Vacancy, PortalHealth, CorrigendumLog
from .notifier import Notifier
from .pdf_parser import GovtNotificationPDFParser

logger = logging.getLogger("medalerts.scraper")

MEDICAL_PATTERN = re.compile(
    r"\b(medical officer|gdmo|cgdmo|cms|combined medical|imo|insurance medical|senior resident|sr\.?\s*resident|junior resident|jr\.?\s*resident|rmo|rmo-cum-tutor|clinical tutor|tutor|demonstrator|specialist|part-time specialist|super specialist|associate consultant|consultant|house staff|house staffship|house-staff|ptmo|health officer|doctor|ayush|bams|bhms|bums|bsms|bnys|homeopath(?:y|ic)?|ayurved(?:a|ic)?|naturopath(?:y|ic)?|contract medical|cmp)\b",
    re.IGNORECASE,
)

RESULT_OR_JOINING_PATTERN = re.compile(
    r"\b(merit\s*list|selected\s*(?:candidates?|list)|shortlisted|waiting\s*list|waitlist|result(?:s)?\s+(?:of|for)|final\s*result|declared\s*result|selection\s*list|provisional\s*(?:list|selection)|final\s*list|joining\s*(?:order|instruction)|offer\s*(?:of\s*appointment|letter)|appointment\s*order|engagement\s*order|empanelment|recommendation\s*list|panel\s*for|cancellation|cancelled)\b",
    re.IGNORECASE,
)

NON_JOB_PATTERN = re.compile(
    r"\b(merit\s*list|selected\s*(?:candidates?|list)|shortlisted|waiting\s*list|waitlist|result(?:s)?\s+(?:of|for)|final\s*result|declared\s*result|selection\s*list|ineligib(?:le|ility)\s*list|list\s*of\s*ineligible|admit\s*cards?|corrigendum|addendum|cancellation|cancelled|answer\s*key|provisional\s*(?:list|selection)|final\s*list|joining\s*(?:order|instruction)|offer\s*(?:of\s*appointment|letter)|appointment\s*order|panel\s*for|engagement\s*order|empanelment|recommendation\s*list|document\s*verification\s*schedule|interview\s*schedule|call\s*letter|list\s*of\s*candidates|closed|guest\s*house|attendant|non[-\s]*medical|field\s*worker|molecular\s*biologist|data\s*management|house\s*staffship\s*committee|selection\s*committee|list\s*for\s*appearing|bachelor['’]?s\s*degree|master['’]?s\s*degree|available\s*services|opd\s*registration|directorate\s*of\s*ayush|dentistry|\bbds\b|\bmds\b|group[-\s]*[cd]|class[-\s]*iv|nursing\s+staff|staff\s+nurse|mining\s+sirdar|overman|surveyor)\b",
    re.IGNORECASE,
)

RECRUITMENT_INTENT_PATTERN = re.compile(
    r"\b(?:recruit(?:ment|ing)?|vacanc(?:y|ies)|engagement|walk[-\s]?in|interview|advertis(?:ement|ing)|advt\.?|notice|notification|circular|applications?\s+(?:are|is)\s+invited|apply\s+online|posts?\s+of|contractual|adhoc|ad[-\s]?hoc|fellowship|corrigendum|memo(?:\s*no)?|rolling\s+adv)\b",
    re.IGNORECASE,
)

_GENERIC_CATEGORY_PATH_RE = re.compile(
    r"/(?:recruitment|recruitments|vacancies|careers|jobs|ayush-departments|senior-resident-and-junior-resident-non-pg-posts-recruitment|courses(?:/[^/]+)*)/?$",
    re.IGNORECASE,
)

PG_ROLE_PATTERN = re.compile(
    r"\b(?:md\s*/\s*ms|m\.?\s*d\.?|m\.?\s*s\.?|dnb|drnb|d\.?\s*m\.?|m\.?\s*ch\.?|pg\s+degree|pg\s+diploma|dgo|dch|dmrd|dlo|doms|dpm|dvd|dtcd|post\s*graduate|post[-\s]*doctoral|fellowships?|icog|senior\s+residents?|sr\.?\s*residents?|specialists?|super\s*specialists?|associate\s+consultants?|consultants?|assistant\s+professors?|associate\s+professors?|professors?|head\s+of\s+department|\bhod\b|faculty|gyna?ecologists?|obstetricians?|surgeons?|physicians?|pa?ediatricians?|radiologists?|pathologists?|ana?esthetists?|ana?esthesiologists?|ophthalmologists?|dermatologists?|psychiatrists?|orthopaed(?:ic|ician)s?|cardiologists?|neurologists?|oncologists?|nephrologists?|urologists?|microbiologists?|biochemists?)\b",
    re.IGNORECASE,
)

MBBS_CORE_PATTERN = re.compile(
    r"\b(?:gdmo|cgdmo|non[-\s]*academic\s+(?:jr\.?|junior\s+resident)|junior\s+resident|jr\.?\s*resident|\bjr\b|house[-\s]?staff|rmo|clinical\s+tutor|tutor|demonstrator|ptmo|health\s+officer|medical\s+officer)\b",
    re.IGNORECASE,
)

PAST_YEAR_LINK_PATTERN = re.compile(r"\b20(?:1\d|2[0-5])\b")
_STALE_URL_DATE_RE = re.compile(r"(?:201\d|202[0-5])")

_TITLE_NUM_DATE_RE = re.compile(r"\b(\d{1,2})[./-](\d{1,2})[./-](20\d{2})\b")
_TITLE_TXT_DATE_RE = re.compile(
    r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?),?\s+(20\d{2})\b",
    re.IGNORECASE,
)


def _clean_notice_title(text: str) -> str:
    t = (text or "").replace("â€¦", "...").replace("â€“", "–").replace("â€”", "—").replace("â€™", "'").replace("â€œ", '"').replace("â€", '"')
    t = re.sub(r"\s*(?:for\s+more\s+details?\s+(?:kindly\s+refer|click\s+the\s+link).*|Downlo(?:ad)?)$", "", t, flags=re.IGNORECASE)
    return " ".join(t.split()).strip(" .,:;")


def _norm_title(title: str) -> str:
    t = _clean_notice_title(title).lower()
    t = re.sub(r"^(?:2nd\s+notice\s+)?(?:online\s+)?applications?\s+(?:are|is)\s+invited\s+(?:online\s+)?(?:from\s+(?:the\s+)?eligible\s+candidates?\s+)?(?:for\s+(?:the\s+)?)?(?:engagement\s+of\s+(?:the\s+)?(?:post\s+of\s+)?)?", "", t)
    t = re.sub(r"^(?:notification\s+for\s+(?:engagement\s+of\s+)?|walk[-\s]?in[-\s]?interview\s+for\s+(?:the\s+)?post\s+of\s+)", "", t)
    return re.sub(r"[^a-z0-9]+", " ", t).strip()[:65]


_DEDUP_STOP_WORDS = {
    "medical", "officer", "recruitment", "notice", "notification", "engagement",
    "post", "posts", "under", "health", "district", "government", "govt", "west",
    "bengal", "india", "contractual", "basis", "walk", "interview", "applications",
    "invited", "eligible", "candidates", "online", "portal", "official", "circular",
}


def _sig_tokens(title: str) -> set:
    return {w for w in re.findall(r"[a-z0-9]{4,}", _clean_notice_title(title).lower()) if w not in _DEDUP_STOP_WORDS}


def _is_fuzzy_duplicate(state: str, tokens: set, seen_token_sets: List[Tuple[str, set]]) -> bool:
    if len(tokens) < 3:
        return False
    st = (state or "").lower()
    for s_state, s_tokens in seen_token_sets:
        s_st = (s_state or "").lower()
        if st and s_st and st != s_st and st != "all india" and s_st != "all india":
            continue
        if len(s_tokens) < 3:
            continue
        overlap = len(tokens & s_tokens)
        if overlap >= 3 and (overlap / min(len(tokens), len(s_tokens))) >= 0.75:
            return True
    return False


def _is_stale_dated_title(text: str, today) -> bool:
    """Returns True if a title's latest explicit date is >45 days in the past."""
    if PAST_YEAR_LINK_PATTERN.search(text or ""):
        return True
    parsed_dates = []
    for d, m, y in _TITLE_NUM_DATE_RE.findall(text or ""):
        try:
            parsed_dates.append(datetime(int(y), int(m), int(d)).date())
        except ValueError:
            pass
    for d, mon, y in _TITLE_TXT_DATE_RE.findall(text or ""):
        for fmt in ("%d %B %Y", "%d %b %Y"):
            try:
                parsed_dates.append(datetime.strptime(f"{int(d)} {mon} {y}", fmt).date())
                break
            except ValueError:
                pass
    if not parsed_dates:
        return False
    latest = max(parsed_dates)
    grace_days = 0 if re.search(r"\b(?:walk[-\s]?in|interview)\b", text or "", re.IGNORECASE) else 15
    return latest < (today - timedelta(days=grace_days))

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
    # --- Defence, Railways & Atomic Energy (Expanded) ---
    {
        "name": "ECHS",
        "organization": "Ex-Servicemen Contributory Health Scheme (ECHS — Medical Officer)",
        "url": "https://www.echs.gov.in/advertisement.php",
        "category": "Defence / Contractual",
        "state": "All India",
        "pay_scale": "₹75,000/month (Fixed Consolidated MO / Specialist)",
    },
    {
        "name": "BARC",
        "organization": "Bhabha Atomic Research Centre (BARC — Medical Officer / SR / Resident)",
        "url": "https://www.barc.gov.in/careers/recruitment.html",
        "category": "Central Govt",
        "state": "Maharashtra",
        "pay_scale": "Level 10 / Level 11 (MO 'C' / 'D' / Resident) + NPA",
    },
    {
        "name": "DRDO_RAC",
        "organization": "DRDO Recruitment & Assessment Centre (RAC)",
        "url": "https://rac.gov.in/",
        "category": "Defence / Central Govt",
        "state": "All India",
        "pay_scale": "Level 10 / Level 11 (Scientist / Medical Officer) + Allowances",
    },
    {
        "name": "Eastern_Railway_RRC",
        "organization": "Eastern Railway (RRC Kolkata — CMP / Medical Officer)",
        "url": "https://rrcer.org/notice_board.html",
        "category": "Railways / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹75,000/month (CMP GDMO) / ₹95,000/month (Specialist)",
    },
    {
        "name": "South_Eastern_Railway_RRC",
        "organization": "South Eastern Railway (RRC-SER Garden Reach — CMP / MO)",
        "url": "https://www.rrcser.co.in/notice.html",
        "category": "Railways / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹75,000/month (CMP GDMO) / ₹95,000/month (Specialist)",
    },
    {
        "name": "Indian_Railways_RRB",
        "organization": "Railway Recruitment Boards (RRB Centralised Portal)",
        "url": "https://www.rrbapply.gov.in/",
        "category": "Railways / Central Govt",
        "state": "All India",
        "pay_scale": "7th CPC Pay Matrix Level 6–10",
    },
    # --- All-India AIIMS & National Institutes (INIs) ---
    {
        "name": "AIIMS_Bhubaneswar",
        "organization": "AIIMS Bhubaneswar (Odisha)",
        "url": "https://aiimsbhubaneswar.nic.in/recruitment-notice/",
        "category": "Autonomous Institute",
        "state": "Odisha",
        "pay_scale": "Level 10 (JR ₹56,100+NPA) / Level 11 (SR ₹67,700+NPA)",
    },
    {
        "name": "AIIMS_Patna",
        "organization": "AIIMS Patna (Bihar)",
        "url": "https://aiimspatna.edu.in/advertisement",
        "category": "Autonomous Institute",
        "state": "Bihar",
        "pay_scale": "Level 10 (JR ₹56,100+NPA) / Level 11 (SR ₹67,700+NPA)",
    },
    {
        "name": "AIIMS_Raipur",
        "organization": "AIIMS Raipur (Chhattisgarh — JR / SR)",
        "url": "https://www.aiimsraipur.edu.in/user/vacancies-faculty.php?pst=jrsr",
        "category": "Autonomous Institute",
        "state": "Chhattisgarh",
        "pay_scale": "Level 10 (JR ₹56,100+NPA) / Level 11 (SR ₹67,700+NPA)",
    },
    {
        "name": "AIIMS_Rishikesh",
        "organization": "AIIMS Rishikesh (Uttarakhand)",
        "url": "https://aiimsrishikesh.edu.in/a1_1/?page_id=2809",
        "category": "Autonomous Institute",
        "state": "Uttarakhand",
        "pay_scale": "Level 10 (JR ₹56,100+NPA) / Level 11 (SR ₹67,700+NPA)",
    },
    {
        "name": "AIIMS_Nagpur",
        "organization": "AIIMS Nagpur (Maharashtra — SR / JR)",
        "url": "https://aiimsnagpur.edu.in/recruitment?category=SR%2FJR",
        "category": "Autonomous Institute",
        "state": "Maharashtra",
        "pay_scale": "Level 10 (JR ₹56,100+NPA) / Level 11 (SR ₹67,700+NPA)",
    },
    {
        "name": "AIIMS_Mangalagiri",
        "organization": "AIIMS Mangalagiri (Andhra Pradesh)",
        "url": "https://www.aiimsmangalagiri.edu.in/whats-new/",
        "category": "Autonomous Institute",
        "state": "Andhra Pradesh",
        "pay_scale": "Level 10 (JR ₹56,100+NPA) / Level 11 (SR ₹67,700+NPA)",
    },
    {
        "name": "AIIMS_Bilaspur",
        "organization": "AIIMS Bilaspur (Himachal Pradesh)",
        "url": "https://www.aiimsbilaspur.edu.in/recruitment",
        "category": "Autonomous Institute",
        "state": "Himachal Pradesh",
        "pay_scale": "Level 10 (JR ₹56,100+NPA) / Level 11 (SR ₹67,700+NPA)",
    },
    {
        "name": "AIIMS_Guwahati",
        "organization": "AIIMS Guwahati (Assam)",
        "url": "https://aiimsguwahati.ac.in/",
        "category": "Autonomous Institute",
        "state": "Assam",
        "pay_scale": "Level 10 (JR ₹56,100+NPA) / Level 11 (SR ₹67,700+NPA)",
    },
    {
        "name": "AIIMS_Jodhpur",
        "organization": "AIIMS Jodhpur (Rajasthan)",
        "url": "https://rec.aiimsjodhpur.edu.in/",
        "category": "Autonomous Institute",
        "state": "Rajasthan",
        "pay_scale": "Level 10 (JR ₹56,100+NPA) / Level 11 (SR ₹67,700+NPA)",
    },
    {
        "name": "AIIMS_Bhopal",
        "organization": "AIIMS Bhopal (Madhya Pradesh)",
        "url": "https://www.aiimsbhopal.edu.in/",
        "category": "Autonomous Institute",
        "state": "Madhya Pradesh",
        "pay_scale": "Level 10 (JR ₹56,100+NPA) / Level 11 (SR ₹67,700+NPA)",
    },
    {
        "name": "AIIMS_Gorakhpur",
        "organization": "AIIMS Gorakhpur (Uttar Pradesh)",
        "url": "https://aiimsgorakhpur.edu.in/",
        "category": "Autonomous Institute",
        "state": "Uttar Pradesh",
        "pay_scale": "Level 10 (JR ₹56,100+NPA) / Level 11 (SR ₹67,700+NPA)",
    },
    {
        "name": "NIMHANS_Bengaluru",
        "organization": "NIMHANS, Bengaluru (Karnataka)",
        "url": "https://www.nimhans.ac.in/announcements/nimhans-recruitment-and-notifications-announcement",
        "category": "Autonomous Institute",
        "state": "Karnataka",
        "pay_scale": "Level 10 (JR / MO) / Level 11 (SR) + NPA",
    },
    # --- Central Maharatna / Navratna PSUs ---
    {
        "name": "IOCL_Careers",
        "organization": "Indian Oil Corporation Limited (IOCL — Medical Officer)",
        "url": "https://iocl.com/latest-job-opening",
        "category": "Central Govt / PSU",
        "state": "All India",
        "pay_scale": "Grade A / B (₹50,000 - ₹1,80,000) + Perks & NPA",
    },
    {
        "name": "NTPC_Careers",
        "organization": "NTPC Limited (GDMO / Medical Specialist)",
        "url": "https://ntpc.co.in/jobs-ntpc",
        "category": "Central Govt / PSU",
        "state": "All India",
        "pay_scale": "E-2 / E-3 Grade (₹50,000 - ₹1,80,000) + Perks",
    },
    {
        "name": "HAL_Careers",
        "organization": "Hindustan Aeronautics Limited (HAL — Medical Officer)",
        "url": "https://hal-india.co.in/career",
        "category": "Central Govt / PSU",
        "state": "All India",
        "pay_scale": "Grade II / III (₹40,000 - ₹1,60,000) + Perks",
    },
    {
        "name": "GAIL_Careers",
        "organization": "GAIL (India) Limited (Medical Officer / GDMO)",
        "url": "https://www.gailonline.com/Vacancies.html",
        "category": "Central Govt / PSU",
        "state": "All India",
        "pay_scale": "E-2 Grade (₹60,000 - ₹1,80,000) + Perks",
    },
    {
        "name": "NHPC_Careers",
        "organization": "NHPC Limited (Medical Officer)",
        "url": "https://www.nhpcindia.com/welcome/job",
        "category": "Central Govt / PSU",
        "state": "All India",
        "pay_scale": "E-2 / E-3 Grade (₹50,000 - ₹1,80,000) + Perks",
    },
    {
        "name": "NMDC_Careers",
        "organization": "NMDC Limited (Medical Officer / Specialist)",
        "url": "https://www.nmdc.co.in/careers",
        "category": "Central Govt / PSU",
        "state": "All India",
        "pay_scale": "E-2 / E-3 Grade (₹60,000 - ₹1,80,000) + Allowances",
    },
    {
        "name": "NALCO_Careers",
        "organization": "National Aluminium Company Limited (NALCO — GDMO / MO)",
        "url": "https://nalcoindia.com/career/",
        "category": "Central Govt / PSU",
        "state": "Odisha",
        "pay_scale": "E-1 / E-2 Grade (₹40,000 - ₹1,60,000) + Perks",
    },
    {
        "name": "ONGC_Careers",
        "organization": "Oil and Natural Gas Corporation (ONGC — Medical Officer)",
        "url": "https://www.ongcindia.com/",
        "category": "Central Govt / PSU",
        "state": "All India",
        "pay_scale": "E-1 / E-2 Grade (₹60,000 - ₹1,80,000) + 35% Perks & NPA",
    },
    {
        "name": "NLC_India",
        "organization": "NLC India Limited (Neyveli — Medical Officer / GDMO)",
        "url": "https://www.nlcindia.in/",
        "category": "Central Govt / PSU",
        "state": "Tamil Nadu",
        "pay_scale": "E-3 Grade (₹60,000 - ₹1,80,000) + Perks",
    },
    {
        "name": "NCL_Singrauli",
        "organization": "Northern Coalfields Limited (NCL — CIL Medical Executive)",
        "url": "https://www.nclcil.in/data-listing/pages/recruitment",
        "category": "Central Govt / PSU",
        "state": "Madhya Pradesh",
        "pay_scale": "E-3 Medical Executive (₹60,000 - ₹1,80,000) + NPA",
    },
    # --- West Bengal Medical Colleges, University & Remaining Districts ---
    {
        "name": "RG_Kar_Kolkata",
        "organization": "R. G. Kar Medical College & Hospital, Kolkata",
        "url": "https://www.rgkarmch.in/page/cms/recruitment_notice_d54b35",
        "category": "WB Medical College (JR / House Staff / RMO)",
        "state": "West Bengal",
        "pay_scale": "WB Govt House Staff / JR Stipend / RMO Pay",
    },
    {
        "name": "WBUHS",
        "organization": "West Bengal University of Health Sciences (WBUHS)",
        "url": "https://wbuhs.ac.in/notice-and-circular/",
        "category": "State University / Medical",
        "state": "West Bengal",
        "pay_scale": "WB Govt / University Pay Scale",
    },
    {
        "name": "BSMC_Bankura",
        "organization": "Bankura Sammilani Medical College & Hospital (BSMC)",
        "url": "https://bsmedicalcollege.org.in/",
        "category": "WB Medical College (JR / House Staff / RMO)",
        "state": "West Bengal",
        "pay_scale": "WB Govt House Staff / JR Stipend / RMO Pay",
    },
    {
        "name": "NBMC_Siliguri",
        "organization": "North Bengal Medical College & Hospital (NBMC), Siliguri",
        "url": "https://www.nbmc.org.in/",
        "category": "WB Medical College (JR / House Staff / RMO)",
        "state": "West Bengal",
        "pay_scale": "WB Govt House Staff / JR Stipend / RMO Pay",
    },
    {
        "name": "MMC_Midnapore",
        "organization": "Midnapore Medical College & Hospital (MMC)",
        "url": "https://midnaporemmc.ac.in/",
        "category": "WB Medical College (JR / House Staff / RMO)",
        "state": "West Bengal",
        "pay_scale": "WB Govt House Staff / JR Stipend / RMO Pay",
    },
    {
        "name": "South_24_Parganas_CMOH",
        "organization": "South 24 Parganas District Health & Family Welfare Samiti (CMOH)",
        "url": "https://s24pgs.gov.in/notice_category/recruitment/",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated NHM / NUHM / FRU)",
    },
    {
        "name": "North_24_Parganas_CMOH",
        "organization": "North 24 Parganas District Health & Family Welfare Samiti (CMOH)",
        "url": "https://north24parganas.gov.in/past-notices/recruitment/",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated NHM / NUHM / FRU)",
    },
    {
        "name": "Hooghly_CMOH",
        "organization": "Hooghly District Health & Family Welfare Samiti (CMOH)",
        "url": "https://hooghly.nic.in/past-notices/recruitment/",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated NHM / NUHM / FRU)",
    },
    {
        "name": "Howrah_CMOH",
        "organization": "Howrah District Health & Family Welfare Samiti (CMOH)",
        "url": "https://howrah.gov.in/notice_category/recruitment/",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated NHM / NUHM / FRU)",
    },
    {
        "name": "Nadia_CMOH",
        "organization": "Nadia District Health & Family Welfare Samiti (CMOH)",
        "url": "https://nadia.gov.in/notice_category/recruitment/",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated NHM / NUHM / FRU)",
    },
    {
        "name": "Murshidabad_CMOH",
        "organization": "Murshidabad District Health & Family Welfare Samiti (CMOH)",
        "url": "https://murshidabad.gov.in/notice_category/recruitment/",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated NHM / NUHM / FRU)",
    },
    {
        "name": "Paschim_Medinipur_CMOH",
        "organization": "Paschim Medinipur District Health & Family Welfare Samiti (CMOH)",
        "url": "https://paschimmedinipur.gov.in/notice_category/recruitment/",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated NHM / NUHM / FRU)",
    },
    {
        "name": "Purba_Medinipur_CMOH",
        "organization": "Purba Medinipur District Health & Family Welfare Samiti (CMOH)",
        "url": "https://purbamedinipur.gov.in/notice_category/recruitment/",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated NHM / NUHM / FRU)",
    },
    {
        "name": "Paschim_Bardhaman_CMOH",
        "organization": "Paschim Bardhaman District Health & Family Welfare Samiti (CMOH)",
        "url": "https://paschimbardhaman.gov.in/past-notices/recruitment/",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated NHM / NUHM / FRU)",
    },
    {
        "name": "Malda_CMOH",
        "organization": "Malda District Health & Family Welfare Samiti (CMOH)",
        "url": "https://malda.gov.in/notice_category/recruitment/",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated NHM / NUHM / FRU)",
    },
    {
        "name": "Darjeeling_CMOH",
        "organization": "Darjeeling District Health & Family Welfare Samiti (CMOH)",
        "url": "https://darjeeling.gov.in/notice_category/recruitment/",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "pay_scale": "₹60,000/month (Consolidated NHM / NUHM / FRU)",
    },
    # --- Major State PSCs & State Medical Recruitment Boards ---
    {
        "name": "OPSC_Odisha",
        "organization": "Odisha Public Service Commission (OPSC — Medical Officer)",
        "url": "https://www.opsc.gov.in/",
        "category": "State PSC",
        "state": "Odisha",
        "pay_scale": "ORSP Level 12 (₹56,100 - ₹1,77,500) + Allowances",
    },
    {
        "name": "BPSC_Bihar",
        "organization": "Bihar Public Service Commission (BPSC — Medical Officer)",
        "url": "https://bpsc.bihar.gov.in/notification-category/notice/",
        "category": "State PSC",
        "state": "Bihar",
        "pay_scale": "Level 9 / Level 11 (Bihar Health Service)",
    },
    {
        "name": "JPSC_Jharkhand",
        "organization": "Jharkhand Public Service Commission (JPSC — Medical Officer)",
        "url": "https://www.jpsc.gov.in/Recruitment.php",
        "category": "State PSC",
        "state": "Jharkhand",
        "pay_scale": "Level 9 / Level 10 (Jharkhand Health Service)",
    },
    {
        "name": "APSC_Assam",
        "organization": "Assam Public Service Commission (APSC — M&HO-I)",
        "url": "https://apscrecruitment.in/",
        "category": "State PSC",
        "state": "Assam",
        "pay_scale": "PB-4 (₹30,000 - ₹1,10,000) + Grade Pay ₹12,700 + NPA",
    },
    {
        "name": "UPPSC_UP",
        "organization": "Uttar Pradesh Public Service Commission (UPPSC — Medical Officer)",
        "url": "https://uppsc.up.nic.in/CandidatePages/Notifications.aspx",
        "category": "State PSC",
        "state": "Uttar Pradesh",
        "pay_scale": "Level 10 / Level 11 (PMHS UP Medical Officer)",
    },
    {
        "name": "MPSC_Maharashtra",
        "organization": "Maharashtra Public Service Commission (MPSC — Medical Officer)",
        "url": "https://mpsc.gov.in/",
        "category": "State PSC",
        "state": "Maharashtra",
        "pay_scale": "S-20 (₹56,100 - ₹1,77,500) + NPA",
    },
    {
        "name": "MPPSC_MP",
        "organization": "Madhya Pradesh Public Service Commission (MPPSC — Medical Officer)",
        "url": "https://mppsc.mp.gov.in/",
        "category": "State PSC",
        "state": "Madhya Pradesh",
        "pay_scale": "Level 12 (₹56,100 - ₹1,77,500) + NPA",
    },
    {
        "name": "RPSC_Rajasthan",
        "organization": "Rajasthan Public Service Commission (RPSC — Medical Officer)",
        "url": "https://rpsc.rajasthan.gov.in/",
        "category": "State PSC",
        "state": "Rajasthan",
        "pay_scale": "Level 14 (Rajasthan Medical & Health Service)",
    },
    {
        "name": "GPSC_Gujarat",
        "organization": "Gujarat Public Service Commission (GPSC — Medical Officer Class-II)",
        "url": "https://gpsc.gujarat.gov.in/",
        "category": "State PSC",
        "state": "Gujarat",
        "pay_scale": "Level 9 / Level 10 (₹53,100 - ₹1,67,800) + NPA",
    },
    {
        "name": "KPSC_Karnataka",
        "organization": "Karnataka Public Service Commission (KPSC — Medical Officer)",
        "url": "https://kpsc.karnataka.gov.in/",
        "category": "State PSC",
        "state": "Karnataka",
        "pay_scale": "Karnataka Health & Family Welfare Pay Scale",
    },
    {
        "name": "Kerala_PSC",
        "organization": "Kerala Public Service Commission (Kerala PSC — Assistant Surgeon)",
        "url": "https://www.keralapsc.gov.in/notifications",
        "category": "State PSC",
        "state": "Kerala",
        "pay_scale": "₹63,700 - ₹1,23,700 (Kerala Health Services)",
    },
    {
        "name": "TN_MRB",
        "organization": "Tamil Nadu Medical Services Recruitment Board (TN MRB — Assistant Surgeon)",
        "url": "https://www.mrb.tn.gov.in/",
        "category": "State PSC / MRB",
        "state": "Tamil Nadu",
        "pay_scale": "Level 22 (₹56,100 - ₹1,77,500) + Allowances",
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
        if "ayush" in low or "ayurved" in low or "homeopath" in low or "unani" in low or "siddha" in low or "naturopath" in low or re.search(r"\b(?:bams|bhms|bums|bsms|bnys)\b", low):
            return {"qualification": "AYUSH", "designation": "AYUSH / BHMS / BAMS Medical Officer"}
        if re.search(r"\b(?:bds|mds|dental|dentistry)\b", low):
            return {"qualification": "BDS", "designation": "Dental Surgeon"}
        # Non-Specialist (GDMO) is explicitly MBBS, even if title says "Non-Specialist consultant(GDMO)"
        if re.search(r"\bnon[-\s]*specialist\b", low):
            return {"qualification": "MBBS", "designation": "Medical Officer / GDMO (Non-Specialist)"}
        # Academic Junior Resident = PG student (MD/MS seat), whereas Non-Academic JR / House Staff = MBBS job
        is_non_acad_jr = bool(re.search(r"\bnon[-\s]*academic\b", low))
        is_acad_jr = bool(re.search(r"\b(?:academic\s+(?:jr\.?|junior\s+resident)|(?:jr\.?|junior\s+resident)\s*\(?\s*academic\s*\)?)\b", low)) and not is_non_acad_jr
        if is_acad_jr:
            return {"qualification": "MD/MS", "designation": "Junior Resident (Academic — PG Seat)"}
        has_pg = bool(PG_ROLE_PATTERN.search(text))
        has_mbbs = bool(MBBS_CORE_PATTERN.search(text))
        if has_pg:
            if re.search(r"\b(?:gdmo|cgdmo|junior\s+resident|jr\.?\s*resident|\bjr\b|non[-\s]*pg|non[-\s]*academic\s+(?:jr\.?|junior\s+resident)|rmo|tutor|demonstrator)\b", low) and "gynecologist" not in low and "gynaecologist" not in low:
                return {"qualification": "MBBS / MD/MS", "designation": "GDMO / Junior Resident & Specialist"}
            return {"qualification": "MD/MS", "designation": "Senior Resident / Specialist / Consultant"}
        if re.search(r"\b(?:rmo|clinical\s+tutor|tutor|demonstrator)\b", low):
            return {"qualification": "MBBS", "designation": "RMO / Clinical Tutor"}
        if re.search(r"\b(?:non[-\s]*academic\s+(?:jr\.?|junior\s+resident)|junior\s+resident|jr\.?\s*resident|\bjr\b|house[-\s]?staff)\b", low):
            return {"qualification": "MBBS", "designation": "Junior Resident (Non-Academic) / House Staff"}
        if has_mbbs:
            return {"qualification": "MBBS", "designation": "Medical Officer / GDMO"}
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

    _GENERIC_LINK_RE = re.compile(
        r"^(?:click\s*here|download(?:\s*pdf|\s*notice|\s*file)?|view(?:\s*details|\s*notice|\s*pdf|\s*more)?|read\s*more|pdf|link|open|details|notice|apply(?:\s*online)?)$",
        re.IGNORECASE,
    )

    @classmethod
    def _extract_candidate_links_with_context(cls, soup: BeautifulSoup, html_text: str, base_url: str) -> List[Tuple[str, str, str]]:
        """Extracts (title, url, row_context) triples from <a> tags, attributes, table/list parents, onclick handlers, and embedded JSON."""
        candidates: List[Tuple[str, str, str]] = []
        for a in soup.find_all("a", href=True):
            text = " ".join(a.get_text(" ", strip=True).split())
            parent_row = a.find_parent("tr") or a.find_parent("li")
            row_text = " ".join(parent_row.get_text(" ", strip=True).split()) if parent_row else ""
            if len(text) < 14 or cls._GENERIC_LINK_RE.match(text):
                attr_text = " ".join((a.get("title") or a.get("aria-label") or "").split())
                if len(attr_text) >= 14 and not cls._GENERIC_LINK_RE.match(attr_text):
                    text = attr_text
                elif len(row_text) >= 14:
                    text = row_text
            candidates.append((text, urljoin(base_url, a["href"].strip()), row_text))

        # Fallback for JS-driven / ASP.NET postback portals using onclick / data-href / data-url
        for el in soup.find_all(attrs={"onclick": True}):
            onclick = el.get("onclick") or ""
            m = re.search(r"(?:window\.open|location\.href\s*=)\s*\(?\s*['\"]([^'\"]+)['\"]", onclick)
            if m:
                text = " ".join((el.get_text(" ", strip=True) or el.get("title") or el.get("aria-label") or "").split())
                parent_row = el.find_parent("tr") or el.find_parent("li")
                row_text = " ".join(parent_row.get_text(" ", strip=True).split()) if parent_row else ""
                if (len(text) < 14 or cls._GENERIC_LINK_RE.match(text)) and len(row_text) >= 14:
                    text = row_text
                if len(text) >= 12:
                    candidates.append((text, urljoin(base_url, m.group(1).strip()), row_text))

        for attr in ("data-href", "data-url", "data-link", "data-file", "data-pdf"):
            for el in soup.find_all(attrs={attr: True}):
                text = " ".join((el.get_text(" ", strip=True) or el.get("title") or el.get("aria-label") or "").split())
                parent_row = el.find_parent("tr") or el.find_parent("li")
                row_text = " ".join(parent_row.get_text(" ", strip=True).split()) if parent_row else ""
                if len(text) >= 12:
                    candidates.append((text, urljoin(base_url, (el.get(attr) or "").strip()), row_text))

        # Fallback for embedded JSON/Next.js/SPA payloads containing PDF links
        for m in re.finditer(
            r'"(?:title|subject|headline|name|noticeTitle|advtTitle|postName|heading)"\s*:\s*"([^"]{12,220})"[^}]{0,280}"(?:url|link|pdf|href|file|path|document|pdfUrl|attachment|filePath|downloadUrl)"\s*:\s*"([^"]+\.pdf[^"]*)"',
            html_text,
            re.IGNORECASE,
        ):
            candidates.append((m.group(1), urljoin(base_url, m.group(2).replace("\\/", "/").strip()), ""))

        # Drop dead anchor/ticker links (e.g. news-announcement.php?, #, javascript:) and prefer .pdf URLs per title
        filtered: List[Tuple[str, str, str]] = []
        for title_txt, href, r_ctx in candidates:
            clean_href = (href or "").strip()
            low_href = clean_href.lower()
            if not low_href or low_href.endswith("?") or low_href.endswith("#") or low_href == "#" or low_href.startswith("javascript:"):
                continue
            filtered.append((title_txt, clean_href, r_ctx))
        filtered.sort(key=lambda triple: 0 if ".pdf" in triple[1].lower() else 1)
        return filtered

    @classmethod
    def _extract_candidate_links(cls, soup: BeautifulSoup, html_text: str, base_url: str) -> List[Tuple[str, str]]:
        """Extracts (title, url) pairs from <a> tags, attributes, table/list parents, onclick handlers, and embedded JSON."""
        return [(t, u) for t, u, _ in cls._extract_candidate_links_with_context(soup, html_text, base_url)]

    _SESSION: Optional[requests.Session] = None
    _PORTAL_CACHE: Dict[str, Dict[str, str]] = {}

    @classmethod
    def _get_session(cls) -> requests.Session:
        if cls._SESSION is None:
            sess = requests.Session()
            retry = Retry(total=2, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504], allowed_methods=["GET"])
            adapter = HTTPAdapter(pool_connections=20, pool_maxsize=20, max_retries=retry)
            sess.mount("https://", adapter)
            sess.mount("http://", adapter)
            cls._SESSION = sess
        return cls._SESSION

    @classmethod
    def fetch_portal_links_with_telemetry(cls, source: Dict[str, str]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        discovered: List[Dict[str, Any]] = []
        t0 = time.monotonic()
        telemetry: Dict[str, Any] = {
            "name": source["name"],
            "organization": source["organization"],
            "url": source["url"],
            "last_status": None,
            "latency_ms": 0,
            "discovered_count": 0,
            "last_error": None,
        }
        try:
            req_headers = dict(cls.HEADERS)
            cached_meta = cls._PORTAL_CACHE.get(source["url"], {})
            if cached_meta.get("etag"):
                req_headers["If-None-Match"] = cached_meta["etag"]
            if cached_meta.get("last_modified"):
                req_headers["If-Modified-Since"] = cached_meta["last_modified"]

            resp = cls._get_session().get(source["url"], headers=req_headers, timeout=7)
            telemetry["last_status"] = resp.status_code
            if resp.status_code == 304:
                telemetry["latency_ms"] = int((time.monotonic() - t0) * 1000)
                return discovered, telemetry
            if not resp.encoding or resp.encoding.lower() == "iso-8859-1":
                resp.encoding = resp.apparent_encoding or "utf-8"
            if not resp.ok:
                logger.warning(f"Portal {source['name']} returned HTTP {resp.status_code}")
                telemetry["last_error"] = f"HTTP {resp.status_code}"
                telemetry["latency_ms"] = int((time.monotonic() - t0) * 1000)
                return discovered, telemetry
            if resp.headers.get("ETag") or resp.headers.get("Last-Modified"):
                meta = {
                    "etag": resp.headers.get("ETag", ""),
                    "last_modified": resp.headers.get("Last-Modified", ""),
                }
                cls._PORTAL_CACHE[source["url"]] = meta
                telemetry["etag"] = meta["etag"]
                telemetry["last_modified"] = meta["last_modified"]

            soup = BeautifulSoup(resp.text, "html.parser")
            if source.get("parser") == "wbhealth_hr_table":
                discovered = cls._parse_wbhealth_hr_table(soup, source)
                telemetry["discovered_count"] = len(discovered)
                telemetry["latency_ms"] = int((time.monotonic() - t0) * 1000)
                return discovered, telemetry

            seen_titles = set()
            pdf_parsed_count = 0
            lifecycle_notices: List[Dict[str, str]] = []
            for text, full_url, row_ctx in cls._extract_candidate_links_with_context(soup, resp.text, source["url"]):
                text = _clean_notice_title(text)
                if len(text) < 12 or len(text) > 260:
                    continue
                low = text.lower()
                is_pdf = ".pdf" in full_url.lower()
                if PAST_YEAR_LINK_PATTERN.search(text):
                    continue
                if MEDICAL_PATTERN.search(text) and RESULT_OR_JOINING_PATTERN.search(text):
                    lifecycle_notices.append({"title": text, "organization": source["organization"], "url": full_url})
                    continue
                if not MEDICAL_PATTERN.search(text) or NON_JOB_PATTERN.search(text):
                    continue
                if not is_pdf:
                    if _GENERIC_CATEGORY_PATH_RE.search(full_url.split("?")[0]):
                        continue
                    if not RECRUITMENT_INTENT_PATTERN.search(f"{text} {row_ctx}"):
                        continue
                if text in seen_titles:
                    continue
                seen_titles.add(text)

                is_walkin = "walk-in" in low or "walk in" in low or "contract" in low
                role_info = cls._infer_role_and_qual(text)
                if role_info["qualification"] == "BDS":
                    continue

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

                pdf_meta: Dict[str, Any] = {}
                parsed: Dict[str, Any] = {}
                if ".pdf" in full_url.lower() and pdf_parsed_count < 15:
                    pdf_parsed_count += 1
                    try:
                        pdf_meta = GovtNotificationPDFParser.extract_from_url_with_meta(full_url)
                        pdf_text = pdf_meta.get("text", "")
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
                        if parsed.get("experience_years_required"):
                            entry["experience_years_required"] = parsed["experience_years_required"]
                        if parsed.get("memo_number"):
                            entry["memo_number"] = parsed["memo_number"]
                        if parsed.get("qualification") in ("MD/MS", "MBBS / MD/MS", "AYUSH", "BDS"):
                            entry["qualification"] = parsed["qualification"]
                        if parsed.get("parsed_confident"):
                            entry["verification_status"] = "VERIFIED_PDF"
                            cadre_note = ""
                            if parsed.get("cadre_breakdown"):
                                cadre_note = " Cadres: " + ", ".join(f"{c['cadre']} ({c['posts']})" for c in parsed["cadre_breakdown"][:4]) + "."
                            entry["summary"] = f"Auto-parsed from official PDF ({parsed.get('memo_number') or source['name']}).{cadre_note} Verify annexures before applying."
                        elif parsed.get("is_scanned"):
                            entry["verification_status"] = "SCANNED_PDF"
                            entry["summary"] = f"Scanned image PDF from {source['organization']}. Open the official PDF directly to verify dates and seats."
                    except Exception as pdf_err:
                        logger.debug(f"PDF auto-parse skipped for {full_url}: {pdf_err}")
                else:
                    t_parsed = GovtNotificationPDFParser.parse_notice_text(text)
                    if t_parsed.get("total_posts"):
                        entry["total_posts"] = t_parsed["total_posts"]
                    else:
                        cnt_m = re.search(r"\bengagement\s+of\s+(\d+)\s*(?:\([a-z]+\))?\s+", text, re.IGNORECASE)
                        if cnt_m:
                            entry["total_posts"] = int(cnt_m.group(1))
                    if t_parsed.get("last_date") and not entry.get("last_date"):
                        entry["last_date"] = datetime.strptime(t_parsed["last_date"], "%Y-%m-%d")

                if entry.get("qualification") == "BDS":
                    continue
                now_ist = datetime.utcnow() + timedelta(hours=5, minutes=30)
                today = now_ist.date()
                if entry.get("last_date") and entry["last_date"] < now_ist:
                    continue
                if entry.get("exam_date") and entry["exam_date"] < now_ist:
                    continue
                if not entry.get("last_date") and not entry.get("exam_date"):
                    if parsed.get("is_stale_document"):
                        continue
                    ref_dt = pdf_meta.get("pdf_creation_date") or pdf_meta.get("last_modified")
                    if ref_dt and ref_dt < (now_ist - timedelta(days=45)):
                        continue
                    if _is_stale_dated_title(f"{text} {row_ctx}", today) or _STALE_URL_DATE_RE.search(full_url):
                        continue

                discovered.append(entry)
                if len(discovered) >= 12:
                    break
        except Exception as e:
            logger.warning(f"Live scrape skipped for {source['name']}: {e}")
            telemetry["last_error"] = str(e)[:250]
        telemetry["discovered_count"] = len(discovered)
        telemetry["lifecycle_notices"] = locals().get("lifecycle_notices", [])
        telemetry["latency_ms"] = int((time.monotonic() - t0) * 1000)
        return discovered, telemetry

    @classmethod
    def fetch_portal_links(cls, source: Dict[str, str]) -> List[Dict[str, Any]]:
        discovered, _ = cls.fetch_portal_links_with_telemetry(source)
        return discovered

    @classmethod
    def close_matching_vacancies_from_notices(cls, db: Session, notices: List[Dict[str, str]]) -> int:
        """Auto-closes active parent vacancies when a portal publishes a matching result, merit list, or joining order."""
        if not notices:
            return 0
        active_rows = db.query(Vacancy).filter(Vacancy.is_active == True).all()
        if not active_rows:
            return 0
        stop_words = {"for", "the", "and", "post", "posts", "of", "in", "under", "with", "to", "medical", "officer", "result", "merit", "list", "joining", "order", "final", "provisional", "selected", "candidates", "notice", "notification", "engagement", "recruitment"}
        closed_count = 0
        for n in notices:
            n_org = (n.get("organization") or "").lower()
            n_title = _clean_notice_title(n.get("title") or "").lower()
            n_tokens = {w for w in re.findall(r"[a-z0-9]{3,}", n_title) if w not in stop_words}
            for row in active_rows:
                if not row.is_active:
                    continue
                if (row.organization or "").lower() != n_org:
                    continue
                if row.memo_number and row.memo_number.split()[0].lower() in n_title:
                    match = True
                else:
                    r_tokens = {w for w in re.findall(r"[a-z0-9]{3,}", (row.title or "").lower()) if w not in stop_words}
                    overlap = len(n_tokens & r_tokens)
                    match = overlap >= 2 or (len(r_tokens) <= 2 and overlap >= 1)
                if match:
                    old_stage = row.stage or "APPLICATION_OPEN"
                    row.is_active = False
                    row.stage = "RESULTS_OUT"
                    row.summary = f"[Results / Joining Order Released] {row.summary or ''}".strip()[:1000]
                    db.add(CorrigendumLog(
                        vacancy_id=row.id,
                        title=row.title,
                        field_changed="stage",
                        old_value=old_stage,
                        new_value="RESULTS_OUT",
                    ))
                    closed_count += 1
        if closed_count:
            db.commit()
        return closed_count

    @classmethod
    def sync_live_portals(cls, db: Session) -> Dict[str, Any]:
        added = 0
        checked_portals = 0
        now = datetime.utcnow()
        now_ist = now + timedelta(hours=5, minutes=30)
        db.query(Vacancy).filter(
            Vacancy.is_active == True,
            Vacancy.last_date.isnot(None),
            Vacancy.last_date < now_ist,
        ).update({"is_active": False, "stage": "APPLICATION_CLOSED"}, synchronize_session=False)
        db.query(Vacancy).filter(
            Vacancy.is_active == True,
            Vacancy.exam_date.isnot(None),
            Vacancy.exam_date < now_ist,
        ).update({"is_active": False, "stage": "INTERVIEW_OVER"}, synchronize_session=False)
        db.query(Vacancy).filter(
            Vacancy.is_active == True,
            Vacancy.last_date.is_(None),
            Vacancy.exam_date.is_(None),
            Vacancy.created_at < now - timedelta(days=7),
        ).update({"is_active": False, "stage": "APPLICATION_CLOSED"}, synchronize_session=False)
        db.commit()

        # Re-classify / deactivate stale, non-medical, dental, or misclassified MD/MS rows already in DB
        today_date = now_ist.date()
        active_rows = db.query(Vacancy).filter(Vacancy.is_active == True).all()
        seen_norm_titles = set()
        seen_token_sets: List[Tuple[str, set]] = []
        undated_pdf_rechecked = 0
        for row in active_rows:
            title_blob = row.title or ""
            summary_blob = f"{title_blob} {row.summary or ''}"
            notif_u = (row.notification_url or "").strip()
            is_bad_non_pdf = bool(notif_u and ".pdf" not in notif_u.lower() and (_GENERIC_CATEGORY_PATH_RE.search(notif_u.split("?")[0]) or not RECRUITMENT_INTENT_PATTERN.search(title_blob)))
            if (not MEDICAL_PATTERN.search(title_blob)) or NON_JOB_PATTERN.search(title_blob) or notif_u.endswith(("?", "#")) or is_bad_non_pdf or (not row.last_date and not row.exam_date and (_is_stale_dated_title(summary_blob, today_date) or _STALE_URL_DATE_RE.search(notif_u))):
                row.is_active = False
                row.stage = "RESULTS_OUT" if RESULT_OR_JOINING_PATTERN.search(title_blob) else "APPLICATION_CLOSED"
                continue
            if not row.last_date and not row.exam_date and ".pdf" in notif_u.lower() and undated_pdf_rechecked < 15:
                undated_pdf_rechecked += 1
                try:
                    pmeta = GovtNotificationPDFParser.extract_from_url_with_meta(notif_u)
                    pparsed = GovtNotificationPDFParser.parse_notice_text(pmeta.get("text", ""))
                    if pparsed.get("last_date"):
                        ld = datetime.strptime(pparsed["last_date"], "%Y-%m-%d")
                        row.last_date = ld
                        if ld < now_ist:
                            row.is_active = False
                            row.stage = "APPLICATION_CLOSED"
                            continue
                    else:
                        ref_dt = pmeta.get("pdf_creation_date") or pmeta.get("last_modified")
                        if pparsed.get("is_stale_document") or (ref_dt and ref_dt < (now_ist - timedelta(days=45))):
                            row.is_active = False
                            row.stage = "APPLICATION_CLOSED"
                            continue
                except Exception:
                    pass
            inferred = cls._infer_role_and_qual(title_blob)
            if inferred["qualification"] == "BDS":
                row.is_active = False
                row.stage = "APPLICATION_CLOSED"
                continue
            elif inferred["qualification"] in ("MD/MS", "AYUSH") and row.qualification in ("MBBS", "MBBS / MD/MS"):
                row.qualification = inferred["qualification"]
                row.designation = inferred["designation"]
            elif inferred["qualification"] == "MBBS / MD/MS" and row.qualification in ("MBBS", "MD/MS"):
                row.qualification = inferred["qualification"]
                row.designation = inferred["designation"]
            elif inferred["qualification"] == "MBBS" and row.qualification in ("MD/MS", "MBBS / MD/MS"):
                row.qualification = inferred["qualification"]
                row.designation = inferred["designation"]
            nt = _norm_title(row.title or "")
            if nt:
                seen_norm_titles.add(nt)
            toks = _sig_tokens(row.title or "")
            if toks:
                seen_token_sets.append((row.state or "", toks))
        db.commit()

        try:
            for ph in db.query(PortalHealth).all():
                if ph.url and (ph.etag or ph.last_modified):
                    cls._PORTAL_CACHE[ph.url] = {"etag": ph.etag or "", "last_modified": ph.last_modified or ""}
        except Exception:
            pass

        all_discovered: List[Dict[str, Any]] = []
        telemetry_batch: List[Dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=12) as executor:
            futures = {executor.submit(cls.fetch_portal_links_with_telemetry, src): src for src in PORTAL_SOURCES}
            for fut in as_completed(futures):
                checked_portals += 1
                src = futures[fut]
                try:
                    items, tel = fut.result()
                    telemetry_batch.append(tel)
                    for item in items:
                        all_discovered.append((src["url"], item))
                except Exception as exc:
                    logger.warning(f"Concurrent fetch failed for {src['name']}: {exc}")
                    telemetry_batch.append({
                        "name": src["name"],
                        "organization": src["organization"],
                        "url": src["url"],
                        "last_status": None,
                        "latency_ms": 0,
                        "discovered_count": 0,
                        "last_error": str(exc)[:250],
                    })

        # Auto-close active vacancies whose Result / Merit List / Joining Order was just published
        all_lifecycle_notices: List[Dict[str, str]] = []
        for tel in telemetry_batch:
            all_lifecycle_notices.extend(tel.get("lifecycle_notices") or [])
        results_closed = cls.close_matching_vacancies_from_notices(db, all_lifecycle_notices)

        # Persist per-portal health telemetry
        for tel in telemetry_batch:
            try:
                ph = db.query(PortalHealth).filter(PortalHealth.name == tel["name"]).first()
                failed = bool(tel.get("last_error")) or (tel.get("last_status") is not None and tel["last_status"] >= 400)
                if not ph:
                    ph = PortalHealth(
                        name=tel["name"],
                        organization=tel["organization"],
                        url=tel["url"],
                        last_status=tel["last_status"],
                        latency_ms=tel["latency_ms"],
                        discovered_count=tel["discovered_count"],
                        consecutive_failures=1 if failed else 0,
                        last_error=tel["last_error"],
                        etag=tel.get("etag"),
                        last_modified=tel.get("last_modified"),
                        last_checked_at=now,
                    )
                    db.add(ph)
                else:
                    ph.organization = tel["organization"]
                    ph.url = tel["url"]
                    ph.last_status = tel["last_status"]
                    ph.latency_ms = tel["latency_ms"]
                    ph.discovered_count = tel["discovered_count"]
                    ph.consecutive_failures = (ph.consecutive_failures or 0) + 1 if failed else 0
                    ph.last_error = tel["last_error"]
                    if tel.get("etag"):
                        ph.etag = tel["etag"]
                    if tel.get("last_modified"):
                        ph.last_modified = tel["last_modified"]
                    ph.last_checked_at = now
            except Exception as ph_err:
                logger.debug(f"PortalHealth update warning for {tel['name']}: {ph_err}")
        db.commit()

        corrigenda_detected = 0
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
            nt = _norm_title(item.get("title", ""))
            toks = _sig_tokens(item.get("title", ""))
            if not existing and ((nt and nt in seen_norm_titles) or _is_fuzzy_duplicate(item.get("state", ""), toks, seen_token_sets)):
                continue
            if existing:
                changes = []
                if item.get("last_date") and item["last_date"] != existing.last_date:
                    old_v = existing.last_date.strftime("%Y-%m-%d") if existing.last_date else "None"
                    new_v = item["last_date"].strftime("%Y-%m-%d")
                    db.add(CorrigendumLog(
                        vacancy_id=existing.id,
                        title=existing.title,
                        field_changed="last_date",
                        old_value=old_v,
                        new_value=new_v,
                    ))
                    changes.append({"field": "last_date", "old": old_v, "new": new_v})
                    existing.last_date = item["last_date"]
                    existing.is_active = True
                if item.get("total_posts") and item["total_posts"] > 0 and existing.total_posts != item["total_posts"]:
                    old_v = str(existing.total_posts or 0)
                    new_v = str(item["total_posts"])
                    db.add(CorrigendumLog(
                        vacancy_id=existing.id,
                        title=existing.title,
                        field_changed="total_posts",
                        old_value=old_v,
                        new_value=new_v,
                    ))
                    changes.append({"field": "total_posts", "old": old_v, "new": new_v})
                    existing.total_posts = item["total_posts"]
                if changes:
                    existing.last_verified_at = now
                    db.commit()
                    Notifier.broadcast_corrigendum(db, existing, changes)
                    corrigenda_detected += 1
                continue
            if nt:
                seen_norm_titles.add(nt)
            if toks:
                seen_token_sets.append((item.get("state", ""), toks))
            v = Vacancy(**item, stage="APPLICATION_OPEN", is_active=True)
            db.add(v)
            db.commit()
            db.refresh(v)
            Notifier.broadcast_new_vacancy(db, v)
            added += 1
        return {"portals_checked": checked_portals, "live_added": added, "corrigenda_detected": corrigenda_detected, "results_closed": results_closed}
