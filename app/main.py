import os
import json
import time
import threading
import requests
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Depends, Query, HTTPException, status, Request, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from .database import engine, Base, get_db
from .models import Vacancy, Subscription, NotificationLog, ExamAttempt
from .collector import VacancyCollector
from .scraper import LiveGazetteScraper
from .notifier import Notifier
from .scheduler import start_scheduler, shutdown_scheduler, scheduler
from .pdf_parser import GovtNotificationPDFParser
from .exam_data import EXAMS_CATALOG, EXAM_QUESTIONS

# Thread-safe in-memory rate limiter & security helpers
_RATE_LOCK = threading.Lock()
_RATE_BUCKETS: Dict[str, List[float]] = {}

def check_rate_limit(request: Request, bucket: str, max_calls: int = 5, window_sec: int = 300):
    client_ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "unknown").split(",")[0].strip()
    key = f"{bucket}:{client_ip}"
    now = time.time()
    with _RATE_LOCK:
        timestamps = [t for t in _RATE_BUCKETS.get(key, []) if now - t < window_sec]
        if len(timestamps) >= max_calls:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded for {bucket}. Please wait a few minutes and try again."
            )
        timestamps.append(now)
        _RATE_BUCKETS[key] = timestamps

def verify_admin_key(x_admin_key: Optional[str] = Header(default=None)):
    expected = os.getenv("ADMIN_API_KEY", "").strip()
    if not expected:
        raise HTTPException(
            status_code=503,
            detail="Admin endpoint is locked. Configure ADMIN_API_KEY in environment variables to enable."
        )
    if x_admin_key != expected:
        raise HTTPException(status_code=403, detail="Invalid or missing X-Admin-Key")

def mask_target(target: str) -> str:
    if not target:
        return "***"
    if "@" in target and not target.startswith("@"):
        local, domain = target.split("@", 1)
        prefix = local[:2] if len(local) >= 2 else local[:1]
        return f"{prefix}***@{domain}"
    if len(target) <= 5:
        return target[:1] + "***"
    return f"{target[:4]}***{target[-2:]}"

# Initialize database schema safely
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Initial Base.metadata.create_all failed: {e}")

app = FastAPI(
    title="MedAlerts - Medical Officer Vacancies Aggregator",
    description="Unified API, automated background poller & eligibility matcher for Medical Officer vacancies.",
    version="2.0.0"
)

# Schemas
class VacancyCreate(BaseModel):
    title: str
    organization: str
    category: str
    state: str = "All India"
    designation: str
    qualification: str = "MBBS"
    total_posts: int = 1
    pay_scale: Optional[str] = "Level 10 Pay Matrix"
    last_date: Optional[datetime] = None
    exam_date: Optional[datetime] = None
    notification_url: Optional[str] = None
    apply_url: Optional[str] = None
    summary: Optional[str] = None
    min_age: int = 21
    max_age: int = 35
    experience_years_required: int = 0
    internship_must_complete: bool = True
    state_registration_mandatory: bool = False
    stage: str = "APPLICATION_OPEN"
    selection_mode: str = "Written Exam + Interview"
    bond_years: int = 0
    bond_penalty_amount: str = "No Bond"
    category_seats_json: Optional[str] = None
    application_fee: str = "As per rules"

class SubscriptionCreate(BaseModel):
    channel: str = Field(..., description="telegram, email, or webhook")
    target: str = Field(..., description="Telegram Chat ID, Email Address, or Webhook URL")
    qualification_filter: str = "ALL"
    state_filter: str = "ALL"
    category_filter: str = "ALL"

class DoctorProfile(BaseModel):
    name: str
    qualification: str = "MBBS"
    college_name: str
    passing_year: int
    internship_status: str = "completed"
    age: int
    category: str = "UR"
    home_state: str = "All India"
    registered_with_smc: bool = True

class PDFAnalyzeURLRequest(BaseModel):
    url: str

class PDFAnalyzeTextRequest(BaseModel):
    text: str

class ExamSubmissionRequest(BaseModel):
    candidate_name: str = "Dr. Candidate"
    answers: Dict[str, Optional[int]] = {}

class TelegramTestRequest(BaseModel):
    chat_id: str
    bot_token: Optional[str] = None

# Mount static directory
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.on_event("startup")
def on_startup():
    from .database import SessionLocal
    try:
        db = SessionLocal()
        try:
            VacancyCollector.sync_sample_feed(db)
        finally:
            db.close()
    except Exception as e:
        print(f"Startup database check notification: {e}")
    
    # Start automated background polling scheduler
    try:
        start_scheduler()
    except Exception as e:
        print(f"Scheduler startup notification: {e}")

@app.on_event("shutdown")
def on_shutdown():
    shutdown_scheduler()

@app.get("/")
@app.head("/")
def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "MedAlerts API is live."}

@app.get("/onboarding")
@app.head("/onboarding")
def serve_onboarding():
    onboarding_file = os.path.join(static_dir, "onboarding.html")
    if os.path.exists(onboarding_file):
        return FileResponse(onboarding_file)
    return {"message": "Onboarding page"}

@app.get("/exam")
@app.head("/exam")
def serve_exam():
    exam_file = os.path.join(static_dir, "exam.html")
    if os.path.exists(exam_file):
        return FileResponse(exam_file)
    return {"message": "Exam Simulator page"}

@app.get("/bonds")
@app.head("/bonds")
def serve_bonds():
    bonds_file = os.path.join(static_dir, "bonds.html")
    if os.path.exists(bonds_file):
        return FileResponse(bonds_file)
    return {"message": "All-India Bond & Pay Matrix page"}

@app.get("/api/health/db")
def health_check_db():
    from urllib.parse import urlparse
    from sqlalchemy import text
    from .database import DATABASE_URL, engine, SessionLocal
    parsed = urlparse(DATABASE_URL)
    host = parsed.hostname or "local-sqlite"
    port = parsed.port
    scheme = parsed.scheme
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            count = db.query(Vacancy).count()
            if count == 0:
                VacancyCollector.sync_sample_feed(db)
                count = db.query(Vacancy).count()
        finally:
            db.close()
        return {
            "status": "ok",
            "driver": scheme,
            "host": host,
            "port": port,
            "vacancies_count": count,
            "message": "Database connection and schema verified!"
        }
    except Exception as e:
        err_str = str(e)
        hint = None
        if "supabase.co" in host and ("Network is unreachable" in err_str or "could not translate host name" in err_str or "timeout" in err_str.lower()):
            hint = "Render Free Tier only supports IPv4, whereas Supabase Direct Connection (db.*.supabase.co) uses IPv6. Switch to Supabase's Pooler URL (*.pooler.supabase.com:6543 or :5432)."
        return {
            "status": "error",
            "driver": scheme,
            "host": host,
            "port": port,
            "error": err_str,
            "hint": hint
        }

@app.get("/api/exams")
def list_exams():
    return EXAMS_CATALOG

@app.get("/api/exams/{exam_id}")
def get_exam_questions(exam_id: str):
    exam_meta = next((e for e in EXAMS_CATALOG if e["id"] == exam_id), None)
    if not exam_meta:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    questions = EXAM_QUESTIONS.get(exam_id, [])
    safe_questions = []
    for q in questions:
        safe_questions.append({
            "id": q["id"],
            "subject": q["subject"],
            "text": q["text"],
            "options": q["options"]
        })
    
    return {
        "exam": exam_meta,
        "questions": safe_questions
    }

@app.post("/api/exams/{exam_id}/submit")
def submit_exam(exam_id: str, payload: ExamSubmissionRequest, db: Session = Depends(get_db)):
    exam_meta = next((e for e in EXAMS_CATALOG if e["id"] == exam_id), None)
    if not exam_meta:
        raise HTTPException(status_code=404, detail="Exam not found")
        
    questions = EXAM_QUESTIONS.get(exam_id, [])
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this exam")
        
    total_q = len(questions)
    marks_per_q = exam_meta["total_marks"] / total_q
    neg_multiplier = exam_meta.get("negative_marking", 0.33)
    
    correct_count = 0
    wrong_count = 0
    unattempted_count = 0
    
    detailed_review = []
    subject_stats = {}
    
    for q in questions:
        subj = q["subject"]
        if subj not in subject_stats:
            subject_stats[subj] = {"total": 0, "correct": 0, "wrong": 0, "unattempted": 0}
        subject_stats[subj]["total"] += 1
        
        user_choice = payload.answers.get(q["id"])
        is_correct = False
        is_attempted = (user_choice is not None)
        
        if not is_attempted:
            unattempted_count += 1
            subject_stats[subj]["unattempted"] += 1
        elif user_choice == q["correct_option"]:
            correct_count += 1
            subject_stats[subj]["correct"] += 1
            is_correct = True
        else:
            wrong_count += 1
            subject_stats[subj]["wrong"] += 1
            
        detailed_review.append({
            "id": q["id"],
            "subject": q["subject"],
            "text": q["text"],
            "options": q["options"],
            "user_choice": user_choice,
            "correct_option": q["correct_option"],
            "is_correct": is_correct,
            "is_attempted": is_attempted,
            "explanation": q.get("explanation", ""),
            "citation": q.get("citation", "")
        })
        
    positive_marks = correct_count * marks_per_q
    negative_marks = wrong_count * marks_per_q * neg_multiplier
    final_score = round(max(0.0, positive_marks - negative_marks), 2)
    accuracy = round((correct_count / (correct_count + wrong_count) * 100), 1) if (correct_count + wrong_count) > 0 else 0
    
    cutoff = exam_meta.get("cutoff_reference", 125)
    qualified = final_score >= cutoff

    attempt_id = None
    try:
        attempt = ExamAttempt(
            exam_id=exam_id,
            exam_title=exam_meta["title"],
            candidate_name=payload.candidate_name[:120],
            final_score=final_score,
            correct=correct_count,
            wrong=wrong_count,
            unattempted=unattempted_count,
            accuracy_pct=accuracy,
            qualified=qualified
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        attempt_id = attempt.id
    except Exception as e:
        print(f"Exam attempt persistence warning: {e}")

    return {
        "attempt_id": attempt_id,
        "candidate_name": payload.candidate_name,
        "exam_title": exam_meta["title"],
        "total_questions": total_q,
        "attempted": correct_count + wrong_count,
        "correct": correct_count,
        "wrong": wrong_count,
        "unattempted": unattempted_count,
        "positive_marks": round(positive_marks, 2),
        "negative_marks": round(negative_marks, 2),
        "final_score": final_score,
        "total_marks": exam_meta["total_marks"],
        "accuracy_pct": accuracy,
        "cutoff_reference": cutoff,
        "qualified": qualified,
        "status_label": "QUALIFIED FOR INTERVIEW" if qualified else "NEEDS REVISION",
        "subject_breakdown": subject_stats,
        "review": detailed_review
    }

@app.get("/api/exams-history")
def list_exam_attempts(limit: int = 10, db: Session = Depends(get_db)):
    rows = db.query(ExamAttempt).order_by(ExamAttempt.created_at.desc()).limit(min(limit, 50)).all()
    return [
        {
            "id": r.id,
            "exam_id": r.exam_id,
            "exam_title": r.exam_title,
            "candidate_name": r.candidate_name,
            "final_score": r.final_score,
            "accuracy_pct": r.accuracy_pct,
            "qualified": r.qualified,
            "created_at": r.created_at.isoformat() if r.created_at else None
        }
        for r in rows
    ]

def _mask_leaderboard_name(name: str) -> str:
    parts = (name or "Dr. Candidate").strip().split()
    if len(parts) <= 1:
        return parts[0] if parts else "Dr. Candidate"
    if parts[0].lower().rstrip(".") == "dr" and len(parts) >= 3:
        return f"{parts[0]} {parts[1]} {parts[-1][0]}."
    return f"{parts[0]} {parts[-1][0]}."

def _clean_ics(val: str) -> str:
    return (val or "").replace("\r", " ").replace("\n", " ").strip()

@app.get("/api/exams/{exam_id}/leaderboard")
def get_exam_leaderboard(exam_id: str, db: Session = Depends(get_db)):
    attempts = db.query(ExamAttempt).filter(ExamAttempt.exam_id == exam_id).order_by(ExamAttempt.final_score.desc()).limit(10).all()
    avg_score = db.query(func.avg(ExamAttempt.final_score)).filter(ExamAttempt.exam_id == exam_id).scalar()
    total_attempts = db.query(func.count(ExamAttempt.id)).filter(ExamAttempt.exam_id == exam_id).scalar() or 0
    return {
        "exam_id": exam_id,
        "total_attempts": total_attempts,
        "peer_average": round(float(avg_score), 2) if avg_score is not None else 0.0,
        "top_scores": [
            {
                "candidate_name": _mask_leaderboard_name(a.candidate_name),
                "final_score": a.final_score,
                "accuracy_pct": a.accuracy_pct,
                "qualified": a.qualified
            }
            for a in attempts
        ]
    }

@app.get("/api/vacancies/{vacancy_id}/calendar.ics")
def download_vacancy_calendar(vacancy_id: str, db: Session = Depends(get_db)):
    v = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    target_dt = v.last_date or (datetime.utcnow() + timedelta(days=7))
    dt_str = target_dt.strftime("%Y%m%dT090000Z")
    dt_end = target_dt.strftime("%Y%m%dT100000Z")
    ics_content = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//MedAlerts//Medical Officer Alerts//EN\r\n"
        "BEGIN:VEVENT\r\n"
        f"UID:{v.id}@medalerts.onrender.com\r\n"
        f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}\r\n"
        f"DTSTART:{dt_str}\r\n"
        f"DTEND:{dt_end}\r\n"
        f"SUMMARY:Deadline: {_clean_ics(v.title)} ({_clean_ics(v.organization)})\r\n"
        f"DESCRIPTION:Qual: {_clean_ics(v.qualification)} | Seats: {v.total_posts} | Apply: {_clean_ics(v.apply_url or '')}\r\n"
        f"URL:{_clean_ics(v.apply_url or 'https://medalerts.onrender.com')}\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
    return Response(
        content=ics_content,
        media_type="text/calendar",
        headers={"Content-Disposition": f"attachment; filename=medalerts-{v.id[:8]}.ics"}
    )

@app.get("/api/stats")
@app.head("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    total_active = db.query(Vacancy).filter(Vacancy.is_active == True).count()
    total_seats = db.query(func.sum(Vacancy.total_posts)).filter(Vacancy.is_active == True).scalar() or 0
    closing_soon = db.query(Vacancy).filter(
        Vacancy.is_active == True,
        Vacancy.last_date <= now + timedelta(days=7),
        Vacancy.last_date >= now
    ).count()
    subscribers_count = db.query(Subscription).filter(Subscription.is_active == True).count()

    return {
        "active_notices": total_active,
        "total_vacancies_seats": int(total_seats),
        "closing_in_7_days": closing_soon,
        "active_subscribers": subscribers_count,
        "scheduler_running": scheduler.running
    }

@app.get("/api/vacancies")
def list_vacancies(
    search: Optional[str] = None,
    qualification: Optional[str] = None,
    category: Optional[str] = None,
    state: Optional[str] = None,
    stage: Optional[str] = None,
    bond: Optional[str] = None,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    query = db.query(Vacancy)

    if active_only:
        query = query.filter(Vacancy.is_active == True)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Vacancy.title.ilike(search_filter),
                Vacancy.organization.ilike(search_filter),
                Vacancy.designation.ilike(search_filter),
                Vacancy.summary.ilike(search_filter)
            )
        )

    if qualification and qualification != "ALL":
        query = query.filter(Vacancy.qualification.ilike(f"%{qualification}%"))

    if category and category != "ALL":
        query = query.filter(Vacancy.category.ilike(f"%{category}%"))

    if state and state != "ALL":
        query = query.filter(or_(Vacancy.state == state, Vacancy.state == "All India"))

    if stage and stage != "ALL":
        query = query.filter(Vacancy.stage == stage)

    if bond == "NO_BOND":
        query = query.filter(Vacancy.bond_years == 0)

    vacancies = query.order_by(Vacancy.last_date.asc()).all()

    results = []
    now = datetime.utcnow()
    for v in vacancies:
        days_left = None
        if v.last_date:
            delta = (v.last_date - now).total_seconds() / 86400.0
            days_left = max(0, int(delta))

        # Parse category seats JSON
        seats_dict = {}
        if v.category_seats_json:
            try:
                seats_dict = json.loads(v.category_seats_json)
            except Exception:
                seats_dict = {}

        results.append({
            "id": v.id,
            "title": v.title,
            "organization": v.organization,
            "category": v.category,
            "state": v.state,
            "designation": v.designation,
            "qualification": v.qualification,
            "total_posts": v.total_posts,
            "pay_scale": v.pay_scale,
            "min_age": v.min_age,
            "max_age": v.max_age,
            "experience_years_required": v.experience_years_required,
            "internship_must_complete": v.internship_must_complete,
            "stage": v.stage,
            "selection_mode": v.selection_mode,
            "bond_years": v.bond_years,
            "bond_penalty_amount": v.bond_penalty_amount,
            "category_seats": seats_dict,
            "application_fee": v.application_fee,
            "last_date": v.last_date.strftime("%Y-%m-%d") if v.last_date else None,
            "exam_date": v.exam_date.strftime("%Y-%m-%d") if v.exam_date else None,
            "days_left": days_left,
            "notification_url": v.notification_url,
            "apply_url": v.apply_url,
            "summary": v.summary,
            "created_at": v.created_at.strftime("%Y-%m-%d") if v.created_at else None
        })

    return results

@app.post("/api/parser/analyze-url")
def analyze_pdf_url(payload: PDFAnalyzeURLRequest, request: Request):
    check_rate_limit(request, "pdf_url", max_calls=10, window_sec=300)
    try:
        text = GovtNotificationPDFParser.extract_from_url(payload.url)
        extracted = GovtNotificationPDFParser.parse_notice_text(text)
        return {"success": True, "extracted": extracted, "data": extracted, "raw_preview": text[:500]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to analyze PDF from URL: {str(e)}")

@app.post("/api/parser/analyze-text")
def analyze_gazette_text(payload: PDFAnalyzeTextRequest):
    extracted = GovtNotificationPDFParser.parse_notice_text(payload.text)
    return {"success": True, "extracted": extracted, "data": extracted}

@app.post("/api/check-eligibility")
def check_eligibility(profile: DoctorProfile, db: Session = Depends(get_db)):
    vacancies = db.query(Vacancy).filter(Vacancy.is_active == True).all()
    results = []
    now = datetime.utcnow()

    age_relaxation = 0
    if profile.category in ["SC", "ST"]:
        age_relaxation = 5
    elif profile.category == "OBC":
        age_relaxation = 3

    current_year = 2026
    approx_experience = max(0, current_year - profile.passing_year)

    for v in vacancies:
        criteria_checks = []
        is_hard_fail = False
        is_conditional = False

        # 1. Qualification Check
        user_qual = profile.qualification.upper()
        req_qual = v.qualification.upper()

        if req_qual == "MD/MS":
            if user_qual == "MD/MS":
                criteria_checks.append({"name": "Qualification", "pass": True, "detail": "Postgraduate Specialist (MD/MS) matched"})
            else:
                is_hard_fail = True
                criteria_checks.append({"name": "Qualification", "pass": False, "detail": "Requires Specialist MD/MS/DNB degree (You have MBBS)"})
        elif req_qual == "AYUSH":
            if user_qual == "AYUSH":
                criteria_checks.append({"name": "Qualification", "pass": True, "detail": "BAMS/BHMS qualification matched"})
            else:
                is_hard_fail = True
                criteria_checks.append({"name": "Qualification", "pass": False, "detail": "Requires AYUSH degree (BAMS / BHMS)"})
        elif req_qual == "BDS":
            if user_qual == "BDS":
                criteria_checks.append({"name": "Qualification", "pass": True, "detail": "Dental (BDS) degree matched"})
            else:
                is_hard_fail = True
                criteria_checks.append({"name": "Qualification", "pass": False, "detail": "Requires BDS degree"})
        else: # MBBS
            if user_qual in ["MBBS", "MD/MS"]:
                criteria_checks.append({"name": "Qualification", "pass": True, "detail": "MBBS degree criterion satisfied"})
            else:
                is_hard_fail = True
                criteria_checks.append({"name": "Qualification", "pass": False, "detail": "Requires basic MBBS degree"})

        # 2. Age Check (with relaxation)
        allowed_max_age = (v.max_age or 35) + age_relaxation
        min_req_age = v.min_age or 21

        if profile.age < min_req_age:
            is_hard_fail = True
            criteria_checks.append({"name": "Age Limit", "pass": False, "detail": f"Underage: Minimum age is {min_req_age} yrs (You are {profile.age})"})
        elif profile.age > allowed_max_age:
            is_hard_fail = True
            criteria_checks.append({"name": "Age Limit", "pass": False, "detail": f"Overage: Max age allowed is {allowed_max_age} yrs for {profile.category} (You are {profile.age})"})
        else:
            relax_msg = f" (incl. {age_relaxation} yrs {profile.category} relaxation)" if age_relaxation > 0 else ""
            criteria_checks.append({"name": "Age Limit", "pass": True, "detail": f"Eligible: Under {allowed_max_age} yrs limit{relax_msg}"})

        # 3. Internship & Experience Check
        if v.experience_years_required > 0:
            if approx_experience < v.experience_years_required:
                is_hard_fail = True
                criteria_checks.append({"name": "Clinical Experience", "pass": False, "detail": f"Requires {v.experience_years_required} yrs experience post-internship (You have ~{approx_experience} yrs)"})
            else:
                criteria_checks.append({"name": "Clinical Experience", "pass": True, "detail": f"Satisfies {v.experience_years_required}+ years post-graduation experience"})
        else:
            criteria_checks.append({"name": "Experience", "pass": True, "detail": "Fresh graduates eligible (0 years experience required)"})

        if v.internship_must_complete:
            if profile.internship_status != "completed":
                is_hard_fail = True
                criteria_checks.append({"name": "Internship", "pass": False, "detail": "Requires completed compulsory rotatory internship before applying"})
            else:
                criteria_checks.append({"name": "Internship", "pass": True, "detail": "Internship completed"})
        else:
            if profile.internship_status != "completed":
                is_conditional = True
                criteria_checks.append({"name": "Internship", "pass": True, "conditional": True, "detail": "Appearing / Interns allowed provisionally (must complete before joining)"})
            else:
                criteria_checks.append({"name": "Internship", "pass": True, "detail": "Internship completed"})

        # 4. State Domicile & Registration Check
        if v.state != "All India" and v.state != profile.home_state:
            if v.state_registration_mandatory:
                is_conditional = True
                criteria_checks.append({"name": "State Registration", "pass": True, "conditional": True, "detail": f"State Council registration with {v.state} Medical Council required before final joining"})
            else:
                criteria_checks.append({"name": "Jurisdiction", "pass": True, "detail": f"All India applicants accepted ({v.state} posting)"})
        else:
            criteria_checks.append({"name": "Jurisdiction", "pass": True, "detail": "Eligible (Home State or All India Cadre)"})

        # 5. Extract reserved seats for this specific candidate category
        user_cat_seats = None
        if v.category_seats_json:
            try:
                s_map = json.loads(v.category_seats_json)
                user_cat_seats = s_map.get(profile.category) or s_map.get("All India Open") or s_map.get("UR")
            except Exception:
                user_cat_seats = None

        if is_hard_fail:
            status_tag = "INELIGIBLE"
            status_label = "Not Eligible"
            badge_color = "red"
        elif is_conditional:
            status_tag = "CONDITIONALLY_ELIGIBLE"
            status_label = "Conditionally Eligible"
            badge_color = "amber"
        else:
            status_tag = "ELIGIBLE"
            status_label = "Fully Eligible to Apply"
            badge_color = "emerald"

        days_left = None
        if v.last_date:
            delta = (v.last_date - now).total_seconds() / 86400.0
            days_left = max(0, int(delta))

        results.append({
            "vacancy_id": v.id,
            "title": v.title,
            "organization": v.organization,
            "category": v.category,
            "state": v.state,
            "designation": v.designation,
            "qualification": v.qualification,
            "total_posts": v.total_posts,
            "user_category_seats": user_cat_seats,
            "pay_scale": v.pay_scale,
            "stage": v.stage,
            "selection_mode": v.selection_mode,
            "bond_penalty_amount": v.bond_penalty_amount,
            "last_date": v.last_date.strftime("%Y-%m-%d") if v.last_date else None,
            "exam_date": v.exam_date.strftime("%Y-%m-%d") if v.exam_date else None,
            "days_left": days_left,
            "apply_url": v.apply_url,
            "notification_url": v.notification_url,
            "status": status_tag,
            "status_label": status_label,
            "badge_color": badge_color,
            "criteria_checks": criteria_checks
        })

    sort_order = {"ELIGIBLE": 0, "CONDITIONALLY_ELIGIBLE": 1, "INELIGIBLE": 2}
    results.sort(key=lambda x: (sort_order[x["status"]], x["days_left"] if x["days_left"] is not None else 999))

    eligible_count = sum(1 for r in results if r["status"] == "ELIGIBLE")
    conditional_count = sum(1 for r in results if r["status"] == "CONDITIONALLY_ELIGIBLE")

    return {
        "candidate": {
            "name": profile.name,
            "qualification": profile.qualification,
            "college": profile.college_name,
            "passing_year": profile.passing_year,
            "age": profile.age,
            "category": profile.category,
            "home_state": profile.home_state
        },
        "summary": {
            "total_evaluated": len(results),
            "fully_eligible": eligible_count,
            "conditionally_eligible": conditional_count,
            "ineligible": len(results) - eligible_count - conditional_count
        },
        "matches": results
    }

@app.post("/api/vacancies", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_admin_key)])
def create_vacancy(payload: VacancyCreate, db: Session = Depends(get_db)):
    vacancy = VacancyCollector.parse_and_add_custom(db, payload.dict())
    return {"message": "Vacancy added and broadcast dispatched", "id": vacancy.id}

@app.post("/api/collector/refresh")
@app.post("/api/sync")
def refresh_collector(request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request, "sync", max_calls=6, window_sec=300)
    result = VacancyCollector.sync_sample_feed(db)
    live = LiveGazetteScraper.sync_live_portals(db)
    return {"message": "Recruitment aggregator executed successfully", **result, **live}

@app.post("/api/subscriptions", status_code=status.HTTP_201_CREATED)
@app.post("/api/subscribe", status_code=status.HTTP_201_CREATED)
def subscribe(payload: SubscriptionCreate, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request, "subscribe", max_calls=10, window_sec=300)
    channel = payload.channel.strip().lower()
    target = payload.target.strip()
    if channel == "telegram":
        is_numeric = target.lstrip("-").isdigit()
        is_channel = target.startswith("@") and len(target) >= 5
        if not (is_numeric or is_channel):
            raise HTTPException(
                status_code=400,
                detail="For Telegram alerts, enter either a numeric Chat ID (get from @userinfobot after sending /start to @MedAlertsRecruitmentBot) or a @channel_username."
            )

    existing = db.query(Subscription).filter(
        Subscription.channel == channel,
        Subscription.target == target
    ).first()

    if existing:
        existing.qualification_filter = payload.qualification_filter
        existing.state_filter = payload.state_filter
        existing.category_filter = payload.category_filter
        existing.is_active = True
        db.commit()
        return {"message": "Subscription updated successfully", "id": existing.id}

    sub = Subscription(
        channel=channel,
        target=target,
        qualification_filter=payload.qualification_filter,
        state_filter=payload.state_filter,
        category_filter=payload.category_filter,
        is_active=True
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return {"message": f"Successfully subscribed to {sub.channel} alerts", "id": sub.id}

@app.get("/api/subscriptions", dependencies=[Depends(verify_admin_key)])
def list_subscriptions(db: Session = Depends(get_db)):
    return db.query(Subscription).all()

@app.get("/api/notifications/recent", dependencies=[Depends(verify_admin_key)])
def list_notifications(limit: int = 15, db: Session = Depends(get_db)):
    logs = db.query(NotificationLog).order_by(NotificationLog.sent_at.desc()).limit(min(limit, 50)).all()
    return [
        {
            "id": l.id,
            "vacancy_id": l.vacancy_id,
            "channel": l.channel,
            "target": mask_target(l.target),
            "sent_at": l.sent_at.isoformat() if l.sent_at else None,
            "status": l.status,
            "details": l.details
        }
        for l in logs
    ]

@app.post("/api/telegram/test")
def test_telegram_broadcast(payload: TelegramTestRequest, request: Request):
    check_rate_limit(request, "telegram_test", max_calls=5, window_sec=300)
    token = (payload.bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "")).strip()
    if not token:
        return {
            "success": False,
            "status": "TOKEN_MISSING",
            "message": "No Telegram Bot Token configured on the server. Set TELEGRAM_BOT_TOKEN in Render or provide it in the test form.",
            "guide": {
                "step1": "Open Telegram and message @BotFather",
                "step2": "Send /newbot and choose a bot name",
                "step3": "Copy the HTTP API Token and add it as TELEGRAM_BOT_TOKEN in your Render dashboard environment variables",
                "step4": "Add your bot as an Administrator to your channel"
            }
        }
    
    # 1. Verify token with Telegram getMe
    try:
        get_me_res = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=8)
        if not get_me_res.ok:
            return {
                "success": False,
                "status": "INVALID_TOKEN",
                "message": f"Telegram API rejected this token: {get_me_res.text}"
            }
        bot_info = get_me_res.json().get("result", {})
    except Exception as e:
        return {"success": False, "status": "NETWORK_ERROR", "message": f"Could not reach Telegram API: {str(e)}"}
    
    # 2. Dispatch a Test Vacancy Alert
    sample_text = (
        f"🩺 <b>MEDALERTS TEST DISPATCH</b>\n\n"
        f"✅ <b>Telegram Integration Verified!</b>\n"
        f"🤖 <b>Bot Name:</b> @{bot_info.get('username')}\n"
        f"📌 <b>Sample Circular:</b> UPSC Combined Medical Services (CMS) 2026\n"
        f"👥 <b>Total Posts:</b> 827 Seats (MBBS)\n"
        f"💰 <b>Pay:</b> Level 10 Matrix (₹56,100 - ₹1,77,500)\n"
        f"📅 <b>Status:</b> Live & Connected to Supabase Database\n\n"
        f"🔗 <a href='https://medalerts.onrender.com'>Open MedAlerts Portal</a>"
    )
    
    try:
        send_res = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={
                "chat_id": payload.chat_id,
                "text": sample_text,
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            },
            timeout=10
        )
        if send_res.ok:
            return {
                "success": True,
                "status": "SENT",
                "bot_username": bot_info.get("username"),
                "recipient": payload.chat_id,
                "message": f"Test message successfully delivered to {payload.chat_id} via @{bot_info.get('username')}!"
            }
        else:
            return {
                "success": False,
                "status": "DELIVERY_FAILED",
                "bot_username": bot_info.get("username"),
                "error_from_telegram": send_res.json(),
                "troubleshooting": "If sending to a public channel, make sure the bot is added as an ADMINISTRATOR with Post Messages permission. If sending to a private user, that user must send /start to the bot first."
            }
    except Exception as e:
        return {"success": False, "status": "SEND_ERROR", "message": str(e)}
