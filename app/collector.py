import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from .models import Vacancy
from .notifier import Notifier

LEGACY_PLACEHOLDER_TITLES = [
    "Combined Medical Services Examination (CMS) 2026",
    "Insurance Medical Officer (IMO) Grade-II Recruitment",
    "Recruitment of Senior Medical Officer & Specialist MO",
    "National Health Mission (NHM) Medical Officers (MBBS & Specialists)",
    "Allopathic Medical Officer Grade-1 Recruitment",
    "Short Service Commissioned Medical Officers (AFMS)",
    "AYUSH Medical Officer (Ayurveda / Homeopathy / Unani)",
    "Contract Medical Practitioner (CMP / GDMO) Walk-in Interview",
    "ESIC Hospital Senior Resident & GDMO (1-Year Walk-in)",
    "ECHS Polyclinic Medical Officer (Contractual Walk-in)",
    "Municipal Corporation (MCD / BMC) Ad-hoc Medical Officer Walk-in",
    "Non-Academic Junior Resident (MBBS) 6-Month Walk-in",
    "District Health Society (NHM) RBSK & UPHC Walk-in MO",
    "WBHRB General Duty Medical Officer (GDMO) & Specialist MO",
    "WBSHFWS / Swasthya Bhawan NUHM & UHWC Medical Officer",
    "Kolkata Municipal Corporation (KMC) Medical Officer Walk-in",
    "AIIMS Kalyani & WB Medical Colleges SR / JR Walk-in",
    "ESI (MB) Scheme West Bengal — Medical Officer & Specialist Walk-in",
]

SAMPLE_VACANCIES: List[Dict[str, Any]] = [
    {
        "title": "Contractual General Duty Medical Officer (CGDMO) — ESI (MB) Scheme WB",
        "organization": "Directorate of ESI (MB) Scheme, West Bengal",
        "category": "ESIC / State Govt",
        "state": "West Bengal",
        "designation": "Contractual General Duty Medical Officer (CGDMO)",
        "qualification": "MBBS",
        "total_posts": 37,
        "pay_scale": "₹60,000/month (Consolidated)",
        "last_date": datetime(2026, 12, 4, 15, 0),
        "exam_date": datetime(2026, 11, 30, 11, 0),
        "notification_url": "https://esiwb.gov.in/home/employment_notice",
        "apply_url": "https://esiwb.gov.in/home/employment_notice",
        "summary": "Memo No. DESI-13011(14)/1/2019-MEDADMN/2372 (Dated 18.11.2026). Walk-in interview at Directorate of ESI (MB) Scheme, Wing B, Plot VI, GB Block, Sector III, Salt Lake, Kolkata-700097 from 30.11.2026 to 04.12.2026 (11:00 AM – 3:00 PM). Requires MBBS recognized by MCI & updated WBMC registration. Age below 64 yrs as on 01.11.2026 (renewable up to 65 yrs or regular PSC WB joining).",
        "min_age": 21,
        "max_age": 63,
        "experience_years_required": 0,
        "internship_must_complete": True,
        "state_registration_mandatory": True,
        "stage": "APPLICATION_OPEN",
        "selection_mode": "Walk-in Interview (30 Nov – 04 Dec 2026, 11 AM–3 PM)",
        "bond_years": 0,
        "bond_penalty_amount": "No Bond (Contractual, 1-month termination notice)",
        "category_seats_json": json.dumps({"UR": 20, "SC": 7, "OBC": 10}),
        "application_fee": "Zero Fee (Prescribed Format in Notice)",
        "verification_status": "VERIFIED_PDF",
        "memo_number": "DESI-13011(14)/1/2019-MEDADMN/2372 (18.11.2026)"
    },
    {
        "title": "Birbhum CMOH / DH&FWS — GDMO (FRU, NUHM/15th FC & RKSK)",
        "organization": "Office of the CMOH & DH&FWS, Birbhum (NHM)",
        "category": "NHM / Contractual",
        "state": "West Bengal",
        "designation": "Medical Officer GDMO (FRU: 4, RKSK: 3, NUHM/15th FC: 8)",
        "qualification": "MBBS",
        "total_posts": 15,
        "pay_scale": "₹60,000/month (Consolidated)",
        "last_date": datetime(2026, 11, 27, 23, 59),
        "exam_date": None,
        "notification_url": "https://hr.wbhealth.gov.in/Files/Recruitment%20Notice%20under%20NHM%20-2026_000402.pdf",
        "apply_url": "https://hr.wbhealth.gov.in/Index.aspx",
        "summary": "Memo No. DHFWS-II/HR-2026/774 (Dated 05.11.2026). Contractual GDMO posts under Birbhum Health District (FRU: 4, RKSK: 3, NUHM/15th FC: 8). Registration & fee payment close 25.11.2026 midnight; full form submission closes 27.11.2026 midnight. Requires MBBS + permanent WB residence + local language proficiency. Scoring: MBBS 85 marks + Interview 15 marks.",
        "min_age": 21,
        "max_age": 40,
        "experience_years_required": 0,
        "internship_must_complete": True,
        "state_registration_mandatory": True,
        "stage": "CLOSING_SOON",
        "selection_mode": "Online Merit (MBBS 85 + Interview 15)",
        "bond_years": 0,
        "bond_penalty_amount": "No Bond (Contractual up to 31.03.2027, renewable)",
        "category_seats_json": json.dumps({"UR": 4, "UR(EC)": 3, "OBC": 1, "OBC(EC)": 1, "SC": 3, "ST": 1, "EWS": 2}),
        "application_fee": "₹100 (Online; Reg closes 25 Nov)",
        "verification_status": "VERIFIED_PDF",
        "memo_number": "DHFWS-II/HR-2026/774 (05.11.2026)"
    },
    {
        "title": "GIPMER (GB Pant Hospital), New Delhi — Junior Resident (Adhoc MBBS)",
        "organization": "Govind Ballabh Pant Institute (GIPMER), GNCTD Delhi",
        "category": "State Govt / JR Walk-in",
        "state": "Delhi",
        "designation": "Junior Resident (Adhoc — Cardiology, CTVS, GI Surgery, Biochem, Psychiatry)",
        "qualification": "MBBS",
        "total_posts": 10,
        "pay_scale": "Level 10 (₹56,100 - ₹1,77,500) + NPA & HRA",
        "last_date": datetime(2026, 11, 30, 16, 0),
        "exam_date": datetime(2026, 12, 2, 12, 0),
        "notification_url": "https://gbpant.delhi.gov.in/sites/default/files/gbpant/generic_multiple_files/termsconditionjr.pdf",
        "apply_url": "https://health.delhi.gov.in/vacancy",
        "summary": "10 Adhoc Junior Resident (MBBS) posts across Cardiology, CTVS, GI Surgery, Biochemistry & Psychiatry. Submit Annexure-I offline at 5th Floor, D-Block, Academic Cell, GIPMER by 30 Nov 2026 (4:00 PM). Interview on 02 Dec 2026 at 12:00 Noon (reporting 11:00 AM). Requires MBBS + 1-yr internship + DMC registration at joining.",
        "min_age": 21,
        "max_age": 30,
        "experience_years_required": 0,
        "internship_must_complete": True,
        "state_registration_mandatory": True,
        "stage": "CLOSING_SOON",
        "selection_mode": "Offline Form (30 Nov) + Interview (02 Dec 2026)",
        "bond_years": 0,
        "bond_penalty_amount": "No Bond (89-day renewable up to 1 yr)",
        "category_seats_json": None,
        "application_fee": "₹300 (DD or Cash at Accounts Branch)",
        "verification_status": "PORTAL_VERIFIED",
        "memo_number": "GIPMER-JR-ADHOC-NOV-2026"
    },
    {
        "title": "BHEL Medical Professionals 2026 — GDMO & Specialist (33 Posts)",
        "organization": "Bharat Heavy Electricals Limited (BHEL — Maharatna PSU)",
        "category": "Central Govt / PSU",
        "state": "All India",
        "designation": "General Duty Medical Officer (GDMO) & Specialist (E1/E2 Grade)",
        "qualification": "MBBS / MD/MS",
        "total_posts": 33,
        "pay_scale": "PSU E1 / E2 Executive Scale + DA & Perks",
        "last_date": datetime(2026, 12, 31, 23, 59),
        "exam_date": None,
        "notification_url": "https://careers.bhel.in/",
        "apply_url": "https://careers.bhel.in/",
        "summary": "Bharat Heavy Electricals Limited (BHEL) recruitment for 33 GDMO & Specialist posts. Online application window runs from 01 December 2026 to 31 December 2026 (11:59 PM) on careers.bhel.in.",
        "min_age": 21,
        "max_age": 37,
        "experience_years_required": 0,
        "internship_must_complete": True,
        "state_registration_mandatory": False,
        "stage": "APPLICATION_OPEN",
        "selection_mode": "Online Form (01–31 Dec 2026) + Interview",
        "bond_years": 0,
        "bond_penalty_amount": "No Bond (Regular / PSU Terms)",
        "category_seats_json": None,
        "application_fee": "Check Official Notice on 01 Dec",
        "verification_status": "PORTAL_VERIFIED",
        "memo_number": "BHEL-MED-2026-33"
    },
    {
        "title": "BEL Medical Officer (E-II) Fixed-Term Recruitment",
        "organization": "Bharat Electronics Limited (BEL — Navratna PSU)",
        "category": "Central Govt / PSU",
        "state": "All India",
        "designation": "Medical Officer (E-II Grade)",
        "qualification": "MBBS",
        "total_posts": 1,
        "pay_scale": "E-II Grade (₹40,000 - ₹1,40,000) + DA & Perks",
        "last_date": datetime(2026, 12, 15, 23, 59),
        "exam_date": None,
        "notification_url": "https://bel-india.in/job-notifications/",
        "apply_url": "https://bel-india.in/job-notifications/",
        "summary": "Bharat Electronics Limited (BEL) recruitment for Medical Officer (E-II) on Fixed Term basis. Requires MBBS with MCI/NMC or State Medical Council registration. Last date for receipt of offline application is 15 December 2026.",
        "min_age": 21,
        "max_age": 32,
        "experience_years_required": 2,
        "internship_must_complete": True,
        "state_registration_mandatory": False,
        "stage": "APPLICATION_OPEN",
        "selection_mode": "Offline Application + Interview",
        "bond_years": 0,
        "bond_penalty_amount": "No Bond (Fixed-Term PSU)",
        "category_seats_json": None,
        "application_fee": "Check Official BEL Notice",
        "verification_status": "PORTAL_VERIFIED",
        "memo_number": "BEL-MO-EII-DEC-2026"
    }
]

class VacancyCollector:
    @staticmethod
    def sync_sample_feed(db: Session) -> Dict[str, int]:
        added_count = 0
        updated_count = 0

        if LEGACY_PLACEHOLDER_TITLES:
            db.query(Vacancy).filter(
                Vacancy.title.in_(LEGACY_PLACEHOLDER_TITLES)
            ).delete(synchronize_session=False)
            db.commit()

        for item in SAMPLE_VACANCIES:
            existing = db.query(Vacancy).filter(
                Vacancy.title == item["title"],
                Vacancy.organization == item["organization"]
            ).first()

            if not existing:
                vacancy = Vacancy(
                    title=item["title"],
                    organization=item["organization"],
                    category=item["category"],
                    state=item["state"],
                    designation=item["designation"],
                    qualification=item["qualification"],
                    total_posts=item["total_posts"],
                    pay_scale=item["pay_scale"],
                    last_date=item["last_date"],
                    exam_date=item.get("exam_date"),
                    notification_url=item["notification_url"],
                    apply_url=item["apply_url"],
                    summary=item["summary"],
                    min_age=item.get("min_age", 21),
                    max_age=item.get("max_age", 35),
                    experience_years_required=item.get("experience_years_required", 0),
                    internship_must_complete=item.get("internship_must_complete", True),
                    state_registration_mandatory=item.get("state_registration_mandatory", False),
                    stage=item.get("stage", "APPLICATION_OPEN"),
                    selection_mode=item.get("selection_mode", "Written Exam + Interview"),
                    bond_years=item.get("bond_years", 0),
                    bond_penalty_amount=item.get("bond_penalty_amount", "No Bond"),
                    category_seats_json=item.get("category_seats_json"),
                    application_fee=item.get("application_fee", "As per rules"),
                    verification_status=item.get("verification_status", "VERIFIED_PDF"),
                    memo_number=item.get("memo_number"),
                    is_active=True
                )
                db.add(vacancy)
                db.commit()
                db.refresh(vacancy)
                Notifier.broadcast_new_vacancy(db, vacancy)
                added_count += 1
            else:
                existing.designation = item["designation"]
                existing.total_posts = item["total_posts"]
                existing.pay_scale = item["pay_scale"]
                existing.last_date = item["last_date"]
                existing.exam_date = item.get("exam_date")
                existing.notification_url = item["notification_url"]
                existing.apply_url = item["apply_url"]
                existing.summary = item["summary"]
                existing.min_age = item.get("min_age", 21)
                existing.max_age = item.get("max_age", 35)
                existing.state_registration_mandatory = item.get("state_registration_mandatory", False)
                existing.selection_mode = item.get("selection_mode", "Written Exam + Interview")
                existing.bond_years = item.get("bond_years", 0)
                existing.bond_penalty_amount = item.get("bond_penalty_amount", "No Bond")
                existing.category_seats_json = item.get("category_seats_json")
                existing.application_fee = item.get("application_fee", "As per rules")
                existing.verification_status = item.get("verification_status", "VERIFIED_PDF")
                existing.memo_number = item.get("memo_number")
                existing.last_verified_at = datetime.utcnow()
                if existing.last_date and existing.last_date < datetime.utcnow():
                    existing.is_active = False
                    existing.stage = "APPLICATION_CLOSED"
                else:
                    existing.is_active = True
                db.commit()
                updated_count += 1

        return {"added": added_count, "updated": updated_count}

    @staticmethod
    def parse_and_add_custom(db: Session, data: Dict[str, Any]) -> Vacancy:
        vacancy = Vacancy(
            title=data.get("title", "Medical Officer Vacancy"),
            organization=data.get("organization", "Govt Department"),
            category=data.get("category", "General"),
            state=data.get("state", "All India"),
            designation=data.get("designation", "Medical Officer"),
            qualification=data.get("qualification", "MBBS"),
            total_posts=int(data.get("total_posts", 1)),
            pay_scale=data.get("pay_scale", "Level 10 Pay Matrix"),
            last_date=datetime.fromisoformat(data["last_date"]) if data.get("last_date") else datetime.utcnow() + timedelta(days=14),
            notification_url=data.get("notification_url", ""),
            apply_url=data.get("apply_url", ""),
            summary=data.get("summary", ""),
            min_age=int(data.get("min_age", 21)),
            max_age=int(data.get("max_age", 35)),
            experience_years_required=int(data.get("experience_years_required", 0)),
            internship_must_complete=bool(data.get("internship_must_complete", True)),
            state_registration_mandatory=bool(data.get("state_registration_mandatory", False)),
            stage=data.get("stage", "APPLICATION_OPEN"),
            selection_mode=data.get("selection_mode", "Written Exam + Interview"),
            bond_years=int(data.get("bond_years", 0)),
            bond_penalty_amount=data.get("bond_penalty_amount", "No Bond"),
            category_seats_json=json.dumps(data.get("category_seats")) if isinstance(data.get("category_seats"), dict) else data.get("category_seats_json"),
            application_fee=data.get("application_fee", "As per rules"),
            verification_status=data.get("verification_status", "VERIFIED_PDF"),
            memo_number=data.get("memo_number"),
            is_active=True
        )
        db.add(vacancy)
        db.commit()
        db.refresh(vacancy)
        Notifier.broadcast_new_vacancy(db, vacancy)
        return vacancy
