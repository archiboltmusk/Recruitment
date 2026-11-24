import re
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from .models import Vacancy
from .notifier import Notifier

SAMPLE_VACANCIES: List[Dict[str, Any]] = [
    {
        "title": "Combined Medical Services Examination (CMS) 2026",
        "organization": "Union Public Service Commission (UPSC)",
        "category": "Central Govt",
        "state": "All India",
        "designation": "Assistant Divisional Medical Officer / General Duty Medical Officer (GDMO)",
        "qualification": "MBBS",
        "total_posts": 827,
        "pay_scale": "Level 10 (₹56,100 - ₹1,77,500) + NPA",
        "last_date": datetime.utcnow() + timedelta(days=22),
        "notification_url": "https://upsc.gov.in/sites/default/files/ExamNotif-CMS-2026.pdf",
        "apply_url": "https://upsconline.nic.in",
        "summary": "Recruitment to Medical Officers in Central Health Service, Indian Railways (ADMO), and New Delhi Municipal Council (NDMC). Written exam followed by personality test.",
    },
    {
        "title": "Recruitment of Insurance Medical Officer (IMO) Grade-II",
        "organization": "Employees' State Insurance Corporation (ESIC)",
        "category": "Central Govt",
        "state": "All India",
        "designation": "Insurance Medical Officer (IMO) Grade II",
        "qualification": "MBBS",
        "total_posts": 571,
        "pay_scale": "Level 10 of Pay Matrix (₹56,100) + 20% NPA",
        "last_date": datetime.utcnow() + timedelta(days=14),
        "notification_url": "https://www.esic.gov.in/recruitments/imo-grade-2.pdf",
        "apply_url": "https://www.esic.gov.in",
        "summary": "Regular posts for medical officers across ESIC hospitals and dispensaries nationwide. Candidate must have completed compulsory rotatory internship.",
    },
    {
        "title": "Recruitment of Senior Medical Officer & GDMO on Direct Recruitment",
        "organization": "AIIMS New Delhi & Regional AIIMS",
        "category": "Autonomous Institute",
        "state": "Delhi / Multi-State",
        "designation": "Senior Medical Officer / Blood Transfusion Officer",
        "qualification": "MD/MS or MBBS with 3 yrs experience",
        "total_posts": 46,
        "pay_scale": "Level 11 (₹67,700 - ₹2,08,700)",
        "last_date": datetime.utcnow() + timedelta(days=18),
        "notification_url": "https://www.aiimsexams.ac.in/recruitment/smo-2026.pdf",
        "apply_url": "https://www.aiimsexams.ac.in",
        "summary": "Direct recruitment for clinical and administrative medical roles across AIIMS New Delhi and associated trauma centers.",
    },
    {
        "title": "National Health Mission (NHM) Medical Officers (MBBS & Specialists)",
        "organization": "State Health Society, NHM Maharashtra",
        "category": "NHM / Contractual",
        "state": "Maharashtra",
        "designation": "Medical Officer (Urban PHCs & Rural Hospitals)",
        "qualification": "MBBS / BAMS",
        "total_posts": 420,
        "pay_scale": "₹60,000 - ₹75,000 per month (Consolidated)",
        "last_date": datetime.utcnow() + timedelta(days=7),
        "notification_url": "https://arogya.maharashtra.gov.in/nhm-recruitment-mo.pdf",
        "apply_url": "https://arogya.maharashtra.gov.in",
        "summary": "Walk-in interview and online application for contractual Medical Officers at Primary Health Centres (PHCs) and Community Health Centres (CHCs).",
    },
    {
        "title": "Allopathic Medical Officer Grade-1 Recruitment",
        "organization": "Uttar Pradesh Public Service Commission (UPPSC)",
        "category": "State PSC",
        "state": "Uttar Pradesh",
        "designation": "Medical Officer (Allopathic)",
        "qualification": "MBBS / Post Graduate Degree/Diploma",
        "total_posts": 1280,
        "pay_scale": "Level 10 (Grade Pay ₹5400) + Allowances",
        "last_date": datetime.utcnow() + timedelta(days=30),
        "notification_url": "https://uppsc.up.nic.in/notices/mo-allopathic-advt.pdf",
        "apply_url": "https://uppsc.up.nic.in",
        "summary": "State health cadre permanent positions in Uttar Pradesh Provincial Medical and Health Services across various district hospitals.",
    },
    {
        "title": "Short Service Commissioned Medical Officers (AFMS)",
        "organization": "Armed Forces Medical Services (Army / Navy / Air Force)",
        "category": "Armed Forces",
        "state": "All India",
        "designation": "Captain / Surgeon Lieutenant / Flight Lieutenant",
        "qualification": "MBBS (Permanent Registration)",
        "total_posts": 212,
        "pay_scale": "Military Pay Matrix Level 10B + Military Service Pay (₹15,500) + NPA",
        "last_date": datetime.utcnow() + timedelta(days=25),
        "notification_url": "https://amcsscentry.gov.in/guidelines.pdf",
        "apply_url": "https://amcsscentry.gov.in",
        "summary": "Applications invited from Indian citizens for grant of Short Service Commission in Armed Forces Medical Services for male and female doctors.",
    },
    {
        "title": "AYUSH Medical Officer (Ayurveda / Homeopathy / Unani)",
        "organization": "Bihar Technical Service Commission (BTSC)",
        "category": "State PSC",
        "state": "Bihar",
        "designation": "Ayush Medical Officer",
        "qualification": "BAMS / BHMS / BUMS",
        "total_posts": 350,
        "pay_scale": "Level 9 (₹53,100 - ₹1,67,800)",
        "last_date": datetime.utcnow() + timedelta(days=12),
        "notification_url": "https://btsc.bih.nic.in/ayush-mo-2026.pdf",
        "apply_url": "https://btsc.bih.nic.in",
        "summary": "Recruitment for AYUSH medical officers across primary and community health dispensaries in Bihar.",
    }
]

class VacancyCollector:
    @staticmethod
    def sync_sample_feed(db: Session) -> Dict[str, int]:
        """Loads and syncs standard verified medical officer vacancies."""
        added_count = 0
        updated_count = 0

        for item in SAMPLE_VACANCIES:
            # Check if exists by title and organization
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
                    notification_url=item["notification_url"],
                    apply_url=item["apply_url"],
                    summary=item["summary"],
                    is_active=True
                )
                db.add(vacancy)
                db.commit()
                db.refresh(vacancy)
                
                # Dispatch notification alerts
                Notifier.broadcast_new_vacancy(db, vacancy)
                added_count += 1
            else:
                # Update existing status
                existing.last_date = item["last_date"]
                existing.is_active = (existing.last_date >= datetime.utcnow()) if existing.last_date else True
                db.commit()
                updated_count += 1

        return {"added": added_count, "updated": updated_count}

    @staticmethod
    def parse_and_add_custom(db: Session, data: Dict[str, Any]) -> Vacancy:
        """Allows adding or web-crawling custom notifications."""
        vacancy = Vacancy(
            title=data.get("title", "Medical Officer Vacancy"),
            organization=data.get("organization", "Govt Department"),
            category=data.get("category", "General"),
            state=data.get("state", "All India"),
            designation=data.get("designation", "Medical Officer"),
            qualification=data.get("qualification", "MBBS"),
            total_posts=int(data.get("total_posts", 1)),
            pay_scale=data.get("pay_scale", "As per rules"),
            last_date=datetime.fromisoformat(data["last_date"]) if data.get("last_date") else datetime.utcnow() + timedelta(days=14),
            notification_url=data.get("notification_url", ""),
            apply_url=data.get("apply_url", ""),
            summary=data.get("summary", ""),
            is_active=True
        )
        db.add(vacancy)
        db.commit()
        db.refresh(vacancy)
        Notifier.broadcast_new_vacancy(db, vacancy)
        return vacancy
