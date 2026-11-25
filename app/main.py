import os
import hmac
import hashlib
import json
import time
import threading
import requests
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Depends, Query, HTTPException, status, Request, Header, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response, HTMLResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from .database import engine, Base, get_db, SessionLocal
from .models import Vacancy, Subscription, NotificationLog, ExamAttempt, PortalHealth, SyncJob, RateLimitBucket, SchemaMigration, DoctorSyncBlob, PushSubscription, CorrigendumLog
from .collector import VacancyCollector
from .scraper import LiveGazetteScraper, PORTAL_SOURCES
from .notifier import Notifier
from .scheduler import start_scheduler, shutdown_scheduler, scheduler
from .pdf_parser import GovtNotificationPDFParser
from .exam_data import EXAMS_CATALOG, EXAM_QUESTIONS

# Thread-safe rate limiter (DB-backed with in-memory fallback) & security helpers
_RATE_LOCK = threading.Lock()
_RATE_BUCKETS: Dict[str, List[float]] = {}
APP_BASE_URL = os.getenv("APP_BASE_URL", "https://medalerts.onrender.com").rstrip("/")

def check_rate_limit(request: Request, bucket: str, max_calls: int = 5, window_sec: int = 300):
    client_ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "unknown").split(",")[0].strip()
    key = f"{bucket}:{client_ip}"
    now = time.time()
    try:
        db = SessionLocal()
        try:
            row = db.query(RateLimitBucket).filter(RateLimitBucket.key == key).first()
            existing_ts = json.loads(row.timestamps_json) if row and row.timestamps_json else []
            timestamps = [t for t in existing_ts if now - t < window_sec]
            if len(timestamps) >= max_calls:
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded for {bucket}. Please wait a few minutes and try again."
                )
            timestamps.append(now)
            if not row:
                db.add(RateLimitBucket(key=key, timestamps_json=json.dumps(timestamps), updated_at=datetime.utcnow()))
            else:
                row.timestamps_json = json.dumps(timestamps)
                row.updated_at = datetime.utcnow()
            db.commit()
            return
        finally:
            db.close()
    except HTTPException:
        raise
    except Exception:
        pass

    with _RATE_LOCK:
        if len(_RATE_BUCKETS) > 1000:
            stale = [k for k, ts in _RATE_BUCKETS.items() if not ts or now - ts[-1] > 86400]
            for k in stale:
                del _RATE_BUCKETS[k]
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
    if not x_admin_key or not hmac.compare_digest(x_admin_key, expected):
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
def ensure_schema():
    from sqlalchemy import text, inspect
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    if "vacancies" in inspector.get_table_names():
        existing_cols = {c["name"] for c in inspector.get_columns("vacancies")}
        migrations = {
            "flag_count": "ALTER TABLE vacancies ADD COLUMN flag_count INTEGER DEFAULT 0",
            "verification_status": "ALTER TABLE vacancies ADD COLUMN verification_status VARCHAR(40) DEFAULT 'NEEDS_PDF_CHECK'",
            "memo_number": "ALTER TABLE vacancies ADD COLUMN memo_number VARCHAR(120)",
            "last_verified_at": "ALTER TABLE vacancies ADD COLUMN last_verified_at TIMESTAMP",
        }
        for col_name, col_sql in migrations.items():
            if col_name not in existing_cols:
                with engine.begin() as conn:
                    conn.execute(text(col_sql))
    db = SessionLocal()
    try:
        for ver in ("001_vacancy_cols", "002_telemetry_ratelimit_syncjob"):
            if not db.query(SchemaMigration).filter(SchemaMigration.version == ver).first():
                db.add(SchemaMigration(version=ver))
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

try:
    ensure_schema()
except Exception as e:
    print(f"Warning: Initial schema check failed: {e}")

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
    verification_status: str = "VERIFIED_PDF"
    memo_number: Optional[str] = None

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
    is_pwbd: bool = False
    attempt_count: int = 0
    dob: Optional[str] = None

class PDFAnalyzeURLRequest(BaseModel):
    url: str

class PDFAnalyzeTextRequest(BaseModel):
    text: str

class PDFAnalyzeFileRequest(BaseModel):
    filename: str = "notice.pdf"
    content_base64: str

class ExamSubmissionRequest(BaseModel):
    candidate_name: str = "Dr. Candidate"
    answers: Dict[str, Optional[int]] = {}

class CheckQuestionRequest(BaseModel):
    question_id: str
    selected_option: int

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
        ensure_schema()
    except Exception as e:
        print(f"Schema migration check: {e}")

    try:
        db = SessionLocal()
        try:
            default_channel = os.getenv("TELEGRAM_DEFAULT_CHANNEL", "@MedAlerts_Official").strip()
            if default_channel:
                existing_sub = db.query(Subscription).filter(
                    Subscription.channel == "telegram",
                    Subscription.target == default_channel
                ).first()
                if not existing_sub:
                    db.add(Subscription(
                        channel="telegram",
                        target=default_channel,
                        qualification_filter="ALL",
                        state_filter="ALL",
                        category_filter="ALL",
                        is_active=True
                    ))
                    db.commit()
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

@app.get("/toolkit")
@app.head("/toolkit")
def serve_toolkit():
    toolkit_file = os.path.join(static_dir, "toolkit.html")
    if os.path.exists(toolkit_file):
        return FileResponse(toolkit_file)
    return {"message": "Post-MBBS Doctor Survival & Career Toolkit"}

@app.get("/admin")
@app.head("/admin")
def serve_admin():
    admin_file = os.path.join(static_dir, "admin.html")
    if os.path.exists(admin_file):
        return FileResponse(admin_file)
    return HTMLResponse("""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Admin Moderation Console — MedAlerts</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-[#F5F5F7] text-[#1D1D1F] min-h-screen">
<header class="sticky top-0 bg-[#F5F5F7]/90 backdrop-blur border-b border-black/10 px-6 h-16 flex items-center justify-between">
  <a href="/" class="font-bold text-base">MedAlerts Admin</a>
  <div class="flex items-center gap-2">
    <input type="password" id="adminKeyInput" placeholder="X-Admin-Key" class="px-3.5 py-1.5 bg-white border border-black/10 rounded-full text-xs">
    <button onclick="saveAndLoad()" class="px-4 py-1.5 rounded-full bg-[#1D1D1F] text-white text-xs font-semibold">Unlock</button>
    <a href="/" class="px-3.5 py-1.5 rounded-full bg-white border border-black/10 text-xs font-semibold">Home</a>
  </div>
</header>
<main class="max-w-5xl mx-auto p-6 space-y-6">
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <div class="bg-white rounded-2xl p-5 space-y-2 border border-black/5">
      <p class="text-xs font-bold uppercase text-[#6E6E73]">Background Sync</p>
      <p id="syncStatusText" class="text-sm font-semibold">Idle</p>
      <button onclick="triggerSync()" class="px-4 py-2 rounded-full bg-[#0F766E] text-white text-xs font-semibold">Run Live Sync</button>
    </div>
    <div class="bg-white rounded-2xl p-5 space-y-2 border border-black/5">
      <p class="text-xs font-bold uppercase text-[#6E6E73]">Telegram Digest</p>
      <p id="digestResult" class="text-xs text-[#6E6E73]">Trigger manual digest</p>
      <button onclick="triggerDigest()" class="px-4 py-2 rounded-full bg-[#1D1D1F] text-white text-xs font-semibold">Broadcast Digest</button>
    </div>
    <div class="bg-white rounded-2xl p-5 space-y-2 border border-black/5">
      <p class="text-xs font-bold uppercase text-[#6E6E73]">Portal Health</p>
      <p id="portalHealthSummary" class="text-sm font-semibold">-</p>
      <button onclick="loadSources()" class="px-4 py-2 rounded-full bg-[#F5F5F7] text-xs font-semibold">Refresh Telemetry</button>
    </div>
  </div>
  <section class="bg-white rounded-2xl p-6 space-y-3 border border-black/5">
    <h2 class="font-bold">Flagged Circulars</h2>
    <div id="flaggedList" class="space-y-2 text-xs text-[#6E6E73]">Unlock with X-Admin-Key to load.</div>
  </section>
  <section class="bg-white rounded-2xl p-6 space-y-3 border border-black/5">
    <h2 class="font-bold">7-Day Discovery &amp; Delivery Metrics</h2>
    <div id="metricsBox" class="text-xs text-[#6E6E73]">Unlock with X-Admin-Key to load analytics.</div>
  </section>
  <section class="bg-white rounded-2xl p-6 space-y-3 border border-black/5">
    <h2 class="font-bold">Recent Notification Logs</h2>
    <div id="logsList" class="space-y-2 text-xs text-[#6E6E73]">Unlock with X-Admin-Key to load.</div>
  </section>
</main>
<script>
function getKey(){return sessionStorage.getItem('med_admin_key')||'';}
function esc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function saveAndLoad(){const v=document.getElementById('adminKeyInput').value.trim();if(v)sessionStorage.setItem('med_admin_key',v);loadFlagged();loadLogs();loadMetrics();loadSources();loadSyncStatus();}
async function loadSyncStatus(){try{const d=await (await fetch('/api/sync/status')).json();document.getElementById('syncStatusText').textContent=`${d.status} • Portals: ${d.portals_checked||0} • Live Added: ${d.live_added||0}`;}catch(e){}}
async function triggerSync(){const d=await (await fetch('/api/sync',{method:'POST'})).json();document.getElementById('syncStatusText').textContent=`${d.status||'STARTED'} (${d.job_id||''})`;setTimeout(loadSyncStatus,3000);}
async function loadSources(){try{const d=await (await fetch('/api/sources')).json();document.getElementById('portalHealthSummary').textContent=`${d.healthy_count||0} / ${d.total||0} Portals Healthy`;}catch(e){}}
async function loadMetrics(){const k=getKey();if(!k)return;const r=await fetch('/api/metrics',{headers:{'X-Admin-Key':k}});const b=document.getElementById('metricsBox');if(!r.ok){b.textContent='Auth error ('+r.status+')';return;}const m=await r.json();b.innerHTML=`<div class='grid grid-cols-2 sm:grid-cols-4 gap-3'><div class='p-3 bg-[#F5F5F7] rounded-xl'><b>${m.active_vacancies}</b><p>Active Jobs</p></div><div class='p-3 bg-[#F5F5F7] rounded-xl'><b>${m.discovered_7d}</b><p>Added (7d)</p></div><div class='p-3 bg-[#F5F5F7] rounded-xl'><b>${m.notifications_success}/${m.notifications_total}</b><p>Alerts Delivered</p></div><div class='p-3 bg-[#F5F5F7] rounded-xl'><b>${(m.failing_portals||[]).length}</b><p>Failing Portals</p></div></div>`;}
async function loadFlagged(){const k=getKey();if(!k)return;const r=await fetch('/api/vacancies/flagged',{headers:{'X-Admin-Key':k}});const b=document.getElementById('flaggedList');if(!r.ok){b.textContent='Auth error ('+r.status+')';return;}const rows=await r.json();b.innerHTML=rows.length?rows.map(x=>`<div class='p-3 bg-[#F5F5F7] rounded-xl flex justify-between items-center'><div><b>${esc(x.title)}</b><p>${esc(x.organization)} • Flags: ${x.flag_count}</p></div>${x.is_active?`<button onclick="deactivate('${esc(x.id)}')" class='px-3 py-1 rounded-full bg-rose-600 text-white font-semibold'>Deactivate</button>`:'Closed'}</div>`).join(''):'No flagged circulars.';}
async function deactivate(id){const r=await fetch(`/api/vacancies/${id}/deactivate`,{method:'POST',headers:{'X-Admin-Key':getKey()}});if(r.ok)loadFlagged();}
async function loadLogs(){const k=getKey();if(!k)return;const r=await fetch('/api/notifications/recent?limit=20',{headers:{'X-Admin-Key':k}});const b=document.getElementById('logsList');if(!r.ok){b.textContent='Auth error ('+r.status+')';return;}const rows=await r.json();b.innerHTML=rows.length?rows.map(l=>`<div class='p-3 bg-[#F5F5F7] rounded-xl flex justify-between'><span><b>${esc(l.channel)}</b> → ${esc(l.target)} • ${esc(l.status)}</span><span>${esc(l.sent_at)}</span></div>`).join(''):'No logs.';}
async function triggerDigest(){const r=await fetch('/api/telegram/broadcast-digest?force=true',{method:'POST',headers:{'X-Admin-Key':getKey()}});document.getElementById('digestResult').textContent=await r.text();}
if(getKey()){document.getElementById('adminKeyInput').value=getKey();saveAndLoad();}else{loadSources();loadSyncStatus();}
</script></body></html>""")

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

def _resolve_exam_and_questions(exam_id: str):
    if exam_id == "image-based":
        all_qs = [q for qs in EXAM_QUESTIONS.values() for q in qs]
        matched = [q for q in all_qs if q.get("image_url")]
        if not matched:
            return None, []
        meta = {
            "id": "image-based",
            "title": "Image-Based Questions (IBQ) — Clinical & Visual Drill",
            "subtitle": f"Clinical, X-ray, anatomy & surgical diagram questions ({len(matched)} Questions)",
            "total_questions": len(matched),
            "total_marks": len(matched),
            "duration_minutes": max(15, len(matched) * 2),
            "negative_marking": 0.33,
            "cutoff_reference": max(1, int(len(matched) * 0.6))
        }
        return meta, matched

    if exam_id.startswith("subject-"):
        slug = exam_id[len("subject-"):].lower()
        all_qs = [q for qs in EXAM_QUESTIONS.values() for q in qs]
        matched = [q for q in all_qs if q["subject"].lower().replace(" ", "-").replace("&", "and") == slug]
        if not matched:
            return None, []
        subj_name = matched[0]["subject"]
        meta = {
            "id": exam_id,
            "title": f"{subj_name} — Focused Drill",
            "subtitle": f"Subject-wise high-yield revision ({len(matched)} Questions)",
            "total_questions": len(matched),
            "total_marks": len(matched),
            "duration_minutes": max(10, len(matched) * 2),
            "negative_marking": 0.33,
            "cutoff_reference": max(1, int(len(matched) * 0.6))
        }
        return meta, matched

    exam_meta = next((e for e in EXAMS_CATALOG if e["id"] == exam_id), None)
    if not exam_meta:
        return None, []
    return exam_meta, EXAM_QUESTIONS.get(exam_id, [])

@app.get("/api/exams")
def list_exams():
    return EXAMS_CATALOG

@app.get("/api/exam-subjects")
def list_exam_subjects():
    counts: Dict[str, int] = {}
    for qs in EXAM_QUESTIONS.values():
        for q in qs:
            counts[q["subject"]] = counts.get(q["subject"], 0) + 1
    return [
        {
            "id": "subject-" + subj.lower().replace(" ", "-").replace("&", "and"),
            "subject": subj,
            "count": cnt
        }
        for subj, cnt in sorted(counts.items(), key=lambda x: -x[1])
    ]

@app.get("/api/exams/{exam_id}")
def get_exam_questions(exam_id: str):
    exam_meta, questions = _resolve_exam_and_questions(exam_id)
    if not exam_meta:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    safe_questions = [
        {"id": q["id"], "subject": q["subject"], "text": q["text"], "options": q["options"], "image_url": q.get("image_url")}
        for q in questions
    ]
    return {"exam": exam_meta, "questions": safe_questions}

@app.post("/api/exams/check-question")
def check_single_question(payload: CheckQuestionRequest):
    for qs in EXAM_QUESTIONS.values():
        for q in qs:
            if q["id"] == payload.question_id:
                is_correct = (payload.selected_option == q["correct_option"])
                return {
                    "question_id": q["id"],
                    "selected_option": payload.selected_option,
                    "correct_option": q["correct_option"],
                    "is_correct": is_correct,
                    "explanation": q.get("explanation", ""),
                    "citation": q.get("citation", "")
                }
    raise HTTPException(status_code=404, detail="Question not found")

@app.post("/api/exams/{exam_id}/submit")
def submit_exam(exam_id: str, payload: ExamSubmissionRequest, db: Session = Depends(get_db)):
    exam_meta, questions = _resolve_exam_and_questions(exam_id)
    if not exam_meta:
        raise HTTPException(status_code=404, detail="Exam not found")
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
            "image_url": q.get("image_url"),
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
    try:
        active_rows = db.query(Vacancy.total_posts, Vacancy.last_date).filter(Vacancy.is_active == True).all()
        total_active = len(active_rows)
        total_seats = sum((r[0] or 0) for r in active_rows)
        cutoff = now + timedelta(days=7)
        closing_soon = sum(1 for r in active_rows if r[1] and now <= r[1] <= cutoff)
    except Exception as e:
        print(f"Stats vacancy query error: {e}")
        total_active, total_seats, closing_soon = 0, 0, 0

    try:
        subscribers_count = db.query(Subscription).filter(Subscription.is_active == True).count()
    except Exception as e:
        print(f"Stats subscription query error: {e}")
        subscribers_count = 0

    return {
        "active_notices": total_active,
        "total_vacancies_seats": int(total_seats),
        "closing_in_7_days": closing_soon,
        "active_subscribers": subscribers_count,
        "scheduler_running": bool(getattr(scheduler, "running", False))
    }

@app.get("/api/sources")
def list_monitored_sources(db: Session = Depends(get_db)):
    health_map = {h.name: h for h in db.query(PortalHealth).all()}
    sources_out = []
    for s in PORTAL_SOURCES:
        h = health_map.get(s["name"])
        sources_out.append({
            "name": s["name"],
            "organization": s["organization"],
            "url": s["url"],
            "category": s["category"],
            "state": s["state"],
            "pay_scale": s["pay_scale"],
            "last_status": h.last_status if h else None,
            "latency_ms": h.latency_ms if h else None,
            "discovered_count": h.discovered_count if h else 0,
            "consecutive_failures": h.consecutive_failures if h else 0,
            "last_error": h.last_error if h else None,
            "last_checked_at": h.last_checked_at.isoformat() if h and h.last_checked_at else None,
        })
    return {
        "total": len(PORTAL_SOURCES),
        "healthy_count": sum(1 for x in sources_out if x["last_status"] and x["last_status"] < 400 and not x["last_error"]),
        "sources": sources_out,
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
    limit: int = Query(default=200, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
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
        if qualification == "MBBS_ONLY":
            query = query.filter(Vacancy.qualification == "MBBS")
        elif qualification.upper() in ("MD/MS/DNB", "MD/MS"):
            query = query.filter(Vacancy.qualification.ilike("%MD/MS%"))
        else:
            query = query.filter(Vacancy.qualification.ilike(f"%{qualification}%"))

    if category and category != "ALL":
        query = query.filter(Vacancy.category.ilike(f"%{category}%"))

    if state and state != "ALL":
        query = query.filter(or_(Vacancy.state == state, Vacancy.state == "All India"))

    if stage and stage != "ALL":
        query = query.filter(Vacancy.stage == stage)

    if bond == "NO_BOND":
        query = query.filter(Vacancy.bond_years == 0)

    vacancies = query.order_by(Vacancy.last_date.asc()).offset(offset).limit(limit).all()

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
            "flag_count": v.flag_count or 0,
            "verification_status": v.verification_status or "NEEDS_PDF_CHECK",
            "memo_number": v.memo_number,
            "last_verified_at": v.last_verified_at.strftime("%d %b %Y") if v.last_verified_at else (v.created_at.strftime("%d %b %Y") if v.created_at else "Today"),
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

@app.post("/api/parser/analyze-file")
def analyze_pdf_file(payload: PDFAnalyzeFileRequest, request: Request):
    import base64
    check_rate_limit(request, "pdf_file", max_calls=15, window_sec=300)
    raw_b64 = (payload.content_base64 or "").strip()
    if "," in raw_b64 and raw_b64.lower().startswith("data:"):
        raw_b64 = raw_b64.split(",", 1)[1]
    try:
        pdf_bytes = base64.b64decode(raw_b64, validate=True)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 PDF payload")
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Uploaded PDF is empty")
    if len(pdf_bytes) > 15 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="PDF file exceeds 15 MB limit")
    try:
        text = GovtNotificationPDFParser.extract_text_from_bytes(pdf_bytes)
        extracted = GovtNotificationPDFParser.parse_notice_text(text)
        return {
            "success": True,
            "filename": payload.filename,
            "extracted": extracted,
            "data": extracted,
            "raw_preview": text[:500],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to analyze uploaded PDF: {str(e)}")

@app.post("/api/check-eligibility")
def check_eligibility(profile: DoctorProfile, db: Session = Depends(get_db)):
    vacancies = db.query(Vacancy).filter(Vacancy.is_active == True).all()
    results = []
    now = datetime.utcnow()

    base_relaxation = 0
    if profile.category in ["SC", "ST"]:
        base_relaxation = 5
    elif profile.category == "OBC":
        base_relaxation = 3
    elif profile.category == "EWS":
        base_relaxation = 0
    elif profile.category == "PwBD":
        base_relaxation = 10
    pwbd_bonus = 10 if (profile.is_pwbd and profile.category != "PwBD") else 0
    age_relaxation = base_relaxation + pwbd_bonus
    effective_age = profile.age
    if profile.dob:
        try:
            dob_dt = datetime.strptime(profile.dob.strip(), "%Y-%m-%d").date()
            today_d = now.date()
            effective_age = today_d.year - dob_dt.year - ((today_d.month, today_d.day) < (dob_dt.month, dob_dt.day))
        except ValueError:
            effective_age = profile.age

    current_year = datetime.utcnow().year
    years_since_pass = max(0, current_year - profile.passing_year)
    approx_experience = max(0, years_since_pass - 1) if (profile.internship_status == "completed" and years_since_pass >= 1) else years_since_pass

    for v in vacancies:
        criteria_checks = []
        is_hard_fail = False
        is_conditional = False

        # 1. Qualification Check (normalize BAMS/BHMS & PG Diploma)
        raw_qual = profile.qualification.upper().strip()
        user_qual = "AYUSH" if any(k in raw_qual for k in ("AYUSH", "BAMS", "BHMS", "BUMS")) else raw_qual
        is_pg_holder = user_qual in ["MD/MS", "PG DIPLOMA"]
        req_qual = v.qualification.upper()

        if "MBBS" in req_qual and "MD/MS" in req_qual:
            if user_qual == "MBBS" or is_pg_holder:
                criteria_checks.append({"name": "Qualification", "pass": True, "detail": "MBBS or MD/MS qualification accepted"})
            else:
                is_hard_fail = True
                criteria_checks.append({"name": "Qualification", "pass": False, "detail": "Requires MBBS or MD/MS degree"})
        elif req_qual == "MD/MS":
            if is_pg_holder:
                criteria_checks.append({"name": "Qualification", "pass": True, "detail": f"Postgraduate Specialist ({profile.qualification}) matched"})
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
            if user_qual == "MBBS" or is_pg_holder:
                criteria_checks.append({"name": "Qualification", "pass": True, "detail": "MBBS degree criterion satisfied"})
            else:
                is_hard_fail = True
                criteria_checks.append({"name": "Qualification", "pass": False, "detail": "Requires basic MBBS degree"})

        # 2. Age Check (with relaxation & unparsed-PDF guard)
        allowed_max_age = (v.max_age or 35) + age_relaxation
        min_req_age = v.min_age or 21
        unparsed_default_age = (v.verification_status == "NEEDS_PDF_CHECK" and not v.memo_number and (v.max_age or 35) == 35)

        if effective_age < min_req_age:
            is_hard_fail = True
            criteria_checks.append({"name": "Age Limit", "pass": False, "detail": f"Underage: Minimum age is {min_req_age} yrs (You are {effective_age})"})
        elif effective_age > allowed_max_age:
            if unparsed_default_age:
                is_conditional = True
                criteria_checks.append({"name": "Age Limit", "pass": True, "conditional": True, "detail": f"Age limit not auto-parsed (default {allowed_max_age} yrs) — verify upper age in official PDF"})
            else:
                is_hard_fail = True
                cat_label = f"{profile.category}{'+PwBD' if profile.is_pwbd and profile.category != 'PwBD' else ''}"
                criteria_checks.append({"name": "Age Limit", "pass": False, "detail": f"Overage: Max age allowed is {allowed_max_age} yrs for {cat_label} (You are {effective_age})"})
        else:
            cat_label = f"{profile.category}{'+PwBD' if profile.is_pwbd and profile.category != 'PwBD' else ''}"
            relax_msg = f" (incl. {age_relaxation} yrs {cat_label} relaxation)" if age_relaxation > 0 else ""
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
        if not profile.registered_with_smc and v.state_registration_mandatory:
            is_conditional = True
            criteria_checks.append({"name": "SMC Registration", "pass": True, "conditional": True, "detail": f"Permanent NMC / {v.state} Medical Council registration required before joining"})
        elif v.state != "All India" and v.state != profile.home_state:
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

def _run_sync_job(job_id: str):
    db = SessionLocal()
    try:
        sample_res = VacancyCollector.sync_sample_feed(db)
        live_res = LiveGazetteScraper.sync_live_portals(db)
        job = db.query(SyncJob).filter(SyncJob.id == job_id).first()
        if job:
            job.status = "COMPLETED"
            job.portals_checked = live_res.get("portals_checked", 0)
            job.live_added = live_res.get("live_added", 0)
            job.sample_added = sample_res.get("added", 0)
            job.finished_at = datetime.utcnow()
            db.commit()
    except Exception as exc:
        job = db.query(SyncJob).filter(SyncJob.id == job_id).first()
        if job:
            job.status = "FAILED"
            job.error = str(exc)[:300]
            job.finished_at = datetime.utcnow()
            db.commit()
    finally:
        db.close()

@app.post("/api/collector/refresh")
@app.post("/api/sync")
def refresh_collector(request: Request, background_tasks: BackgroundTasks, background: bool = True, db: Session = Depends(get_db)):
    check_rate_limit(request, "sync", max_calls=2, window_sec=300)
    if not background:
        result = VacancyCollector.sync_sample_feed(db)
        live = LiveGazetteScraper.sync_live_portals(db)
        return {"message": "Recruitment aggregator executed successfully", **result, **live}
    job = SyncJob(status="RUNNING")
    db.add(job)
    db.commit()
    db.refresh(job)
    background_tasks.add_task(_run_sync_job, job.id)
    return {"message": "Background sync started", "job_id": job.id, "status": "RUNNING"}

@app.get("/api/sync/status")
def get_sync_status(job_id: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(SyncJob)
    job = q.filter(SyncJob.id == job_id).first() if job_id else q.order_by(SyncJob.started_at.desc()).first()
    if not job:
        return {"status": "IDLE", "message": "No sync jobs recorded yet"}
    return {
        "job_id": job.id,
        "status": job.status,
        "portals_checked": job.portals_checked,
        "live_added": job.live_added,
        "sample_added": job.sample_added,
        "error": job.error,
        "started_at": job.started_at.isoformat() if job.started_at else None,
        "finished_at": job.finished_at.isoformat() if job.finished_at else None,
    }

@app.post("/api/subscriptions", status_code=status.HTTP_201_CREATED)
@app.post("/api/subscribe", status_code=status.HTTP_201_CREATED)
def subscribe(payload: SubscriptionCreate, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request, "subscribe", max_calls=10, window_sec=300)
    channel = payload.channel.strip().lower()
    target = payload.target.strip()
    if channel not in ("telegram", "email", "webhook"):
        raise HTTPException(status_code=400, detail="Channel must be telegram, email, or webhook.")
    if channel == "webhook" and not GovtNotificationPDFParser.is_safe_url(target):
        raise HTTPException(status_code=400, detail="Webhook URL must be a valid public http(s) endpoint.")
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

@app.post("/api/vacancies/{vacancy_id}/flag")
def flag_vacancy_issue(vacancy_id: str, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request, f"flag:{vacancy_id}", max_calls=1, window_sec=86400)
    v = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    v.flag_count = (v.flag_count or 0) + 1
    if v.flag_count >= 3 and v.stage != "APPLICATION_CLOSED":
        v.stage = "NEEDS_VERIFICATION"
    db.commit()
    return {"message": "Circular flagged for verification review", "flag_count": v.flag_count}

@app.get("/api/vacancies/flagged", dependencies=[Depends(verify_admin_key)])
def list_flagged_vacancies(db: Session = Depends(get_db)):
    rows = db.query(Vacancy).filter(or_(Vacancy.flag_count > 0, Vacancy.stage == "NEEDS_VERIFICATION")).order_by(Vacancy.flag_count.desc()).all()
    return [{"id": v.id, "title": v.title, "organization": v.organization, "flag_count": v.flag_count or 0, "stage": v.stage, "is_active": v.is_active} for v in rows]

@app.post("/api/vacancies/{vacancy_id}/deactivate", dependencies=[Depends(verify_admin_key)])
def deactivate_vacancy(vacancy_id: str, db: Session = Depends(get_db)):
    v = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    v.is_active = False
    v.stage = "APPLICATION_CLOSED"
    db.commit()
    return {"message": "Vacancy deactivated", "id": v.id}

@app.post("/api/telegram/broadcast-digest", dependencies=[Depends(verify_admin_key)])
def trigger_telegram_digest(force: bool = False, db: Session = Depends(get_db)):
    return Notifier.broadcast_daily_digest(db, force=force)

@app.post("/api/telegram/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
):
    secret = os.getenv("TELEGRAM_WEBHOOK_SECRET", "").strip()
    if secret and (not x_telegram_bot_api_secret_token or not hmac.compare_digest(x_telegram_bot_api_secret_token, secret)):
        raise HTTPException(status_code=403, detail="Invalid webhook secret")
    update = await request.json()
    msg = update.get("message") or update.get("edited_message") or {}
    chat_id = (msg.get("chat") or {}).get("id")
    text = msg.get("text") or ""
    if not chat_id:
        return {"ok": True, "ignored": True}
    reply = Notifier.handle_telegram_command(db, str(chat_id), text)
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if token:
        try:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": reply, "parse_mode": "HTML"},
                timeout=8,
            )
        except Exception:
            pass
    return {"ok": True, "reply": reply}

class ProfileSyncPayload(BaseModel):
    sync_key: str = Field(..., min_length=6, max_length=64)
    payload: Dict[str, Any]

def _hash_sync_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.strip().encode("utf-8")).hexdigest()

@app.post("/api/profile/sync")
def save_cloud_profile(body: ProfileSyncPayload, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request, "profile_sync", max_calls=20, window_sec=300)
    hashed = _hash_sync_key(body.sync_key)
    raw_json = json.dumps(body.payload)[:100000]
    row = db.query(DoctorSyncBlob).filter(DoctorSyncBlob.sync_key == hashed).first()
    if not row:
        db.add(DoctorSyncBlob(sync_key=hashed, payload_json=raw_json, updated_at=datetime.utcnow()))
    else:
        row.payload_json = raw_json
        row.updated_at = datetime.utcnow()
    db.commit()
    return {"ok": True, "updated_at": datetime.utcnow().isoformat()}

@app.get("/api/profile/sync/{sync_key}")
def load_cloud_profile(sync_key: str, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request, "profile_sync_read", max_calls=20, window_sec=300)
    if len(sync_key.strip()) < 6:
        raise HTTPException(status_code=400, detail="Sync key must be at least 6 characters")
    hashed = _hash_sync_key(sync_key)
    row = db.query(DoctorSyncBlob).filter(DoctorSyncBlob.sync_key == hashed).first()
    if not row:
        raise HTTPException(status_code=404, detail="No synced backup found for this key")
    return {"ok": True, "payload": json.loads(row.payload_json or "{}"), "updated_at": row.updated_at.isoformat() if row.updated_at else None}

@app.get("/manifest.json")
def pwa_manifest():
    manifest = {
        "name": "MedAlerts — Medical Officer Jobs & Mock CBT",
        "short_name": "MedAlerts",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#F5F5F7",
        "theme_color": "#0F766E",
        "icons": [
            {
                "src": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%230F766E'/%3E%3Ctext x='50%25' y='55%25' font-size='34' text-anchor='middle' fill='white'%3E%E2%9A%95%3C/text%3E%3C/svg%3E",
                "sizes": "192x192",
                "type": "image/svg+xml",
            }
        ],
    }
    return Response(content=json.dumps(manifest), media_type="application/manifest+json")

def _unsub_token(sub_id: int, target: str) -> str:
    sec = (os.getenv("ADMIN_API_KEY") or os.getenv("TELEGRAM_BOT_TOKEN") or "medalerts-unsub").encode("utf-8")
    return hmac.new(sec, f"{sub_id}:{target}".encode("utf-8"), hashlib.sha256).hexdigest()[:24]

@app.get("/api/unsubscribe")
def unsubscribe_email(id: int, token: str, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == id).first()
    if not sub or not hmac.compare_digest(_unsub_token(sub.id, sub.target), (token or "").strip()):
        raise HTTPException(status_code=403, detail="Invalid or expired unsubscribe link")
    sub.is_active = False
    db.commit()
    return HTMLResponse("<html><body style='font-family:sans-serif;padding:40px;text-align:center'><h2>Unsubscribed from MedAlerts</h2><p>You will no longer receive email alerts for this subscription.</p><a href='/'>Back to MedAlerts</a></body></html>")

@app.get("/api/metrics", dependencies=[Depends(verify_admin_key)])
def get_admin_metrics(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    active_vacancies = db.query(Vacancy).filter(Vacancy.is_active == True).count()
    discovered_7d = db.query(Vacancy).filter(Vacancy.created_at >= week_ago).count()
    notif_total = db.query(NotificationLog).count()
    notif_ok = db.query(NotificationLog).filter(NotificationLog.status == "SUCCESS").count()
    failing = db.query(PortalHealth).filter(PortalHealth.consecutive_failures > 0).order_by(PortalHealth.consecutive_failures.desc()).limit(10).all()
    return {
        "active_vacancies": active_vacancies,
        "discovered_7d": discovered_7d,
        "notifications_total": notif_total,
        "notifications_success": notif_ok,
        "failing_portals": [{"name": p.name, "failures": p.consecutive_failures, "error": p.last_error} for p in failing],
    }

@app.get("/sw.js")
def pwa_service_worker():
    sw_code = """const CACHE = 'medalerts-v2';
const SHELL = ['/', '/onboarding', '/exam', '/bonds', '/toolkit'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).catch(()=>{})); self.skipWaiting(); });
self.addEventListener('activate', e => { e.waitUntil(self.clients.claim()); });
self.addEventListener('push', e => {
  const d = e.data ? e.data.json() : { title: 'MedAlerts', body: 'New Medical Officer recruitment alert', url: '/' };
  e.waitUntil(self.registration.showNotification(d.title || 'MedAlerts', { body: d.body || '', data: { url: d.url || '/' } }));
});
self.addEventListener('notificationclick', e => {
  e.notification.close();
  e.waitUntil(clients.openWindow((e.notification.data && e.notification.data.url) || '/'));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(fetch(e.request).then(r => {
    if (r.ok && e.request.url.startsWith(self.location.origin)) {
      const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)).catch(()=>{});
    }
    return r;
  }).catch(() => caches.match(e.request)));
});"""
    return Response(content=sw_code, media_type="application/javascript")

@app.get("/feed.xml")
def rss_feed(db: Session = Depends(get_db)):
    from html import escape
    rows = db.query(Vacancy).filter(Vacancy.is_active == True).order_by(Vacancy.created_at.desc()).limit(30).all()
    items = []
    for v in rows:
        link = f"{APP_BASE_URL}/?job={escape(str(v.id), quote=True)}"
        pub_str = (v.created_at or datetime.utcnow()).strftime("%a, %d %b %Y %H:%M:%S +0000")
        desc = escape(f"{v.organization} • {v.qualification} • {v.total_posts} Posts • {v.state}", quote=True)
        items.append(f"<item><title>{escape(v.title or '', quote=True)}</title><link>{link}</link><guid>{link}</guid><pubDate>{pub_str}</pubDate><description>{desc}</description></item>")
    xml_body = '<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>MedAlerts Vacancies</title>' + f'<link>{escape(APP_BASE_URL, quote=True)}/</link><description>Medical Officer recruitment circulars</description>' + "".join(items) + "</channel></rss>"
    return Response(content=xml_body, media_type="application/rss+xml")

@app.get("/sitemap.xml")
def sitemap_xml(db: Session = Depends(get_db)):
    from html import escape
    static_paths = ["", "/onboarding", "/exam", "/bonds", "/toolkit"]
    urls = [f"<url><loc>{escape(APP_BASE_URL + p, quote=True)}</loc><changefreq>daily</changefreq></url>" for p in static_paths]
    rows = db.query(Vacancy.id, Vacancy.created_at).filter(Vacancy.is_active == True).order_by(Vacancy.created_at.desc()).limit(200).all()
    for v_id, created_at in rows:
        lastmod = f"<lastmod>{created_at.strftime('%Y-%m-%d')}</lastmod>" if created_at else ""
        urls.append(f"<url><loc>{escape(f'{APP_BASE_URL}/?job={v_id}', quote=True)}</loc>{lastmod}<changefreq>daily</changefreq></url>")
    ns = "http://" + "www.sitemaps.org/schemas/sitemap/0.9"
    xml_body = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="{ns}">' + "".join(urls) + "</urlset>"
    return Response(content=xml_body, media_type="application/xml")

class PushSubscribeRequest(BaseModel):
    endpoint: str
    keys: Optional[Dict[str, str]] = None
    qualification_filter: str = "ALL"
    state_filter: str = "ALL"

@app.post("/api/push/subscribe", status_code=status.HTTP_201_CREATED)
def save_push_subscription(payload: PushSubscribeRequest, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request, "push_sub", max_calls=15, window_sec=300)
    endpoint = (payload.endpoint or "").strip()
    if not endpoint.startswith("https://"):
        raise HTTPException(status_code=400, detail="Invalid push subscription endpoint")
    keys = payload.keys or {}
    row = db.query(PushSubscription).filter(PushSubscription.endpoint == endpoint).first()
    if not row:
        row = PushSubscription(
            endpoint=endpoint,
            p256dh=keys.get("p256dh"),
            auth=keys.get("auth"),
            qualification_filter=payload.qualification_filter,
            state_filter=payload.state_filter,
            is_active=True,
        )
        db.add(row)
    else:
        row.p256dh = keys.get("p256dh") or row.p256dh
        row.auth = keys.get("auth") or row.auth
        row.qualification_filter = payload.qualification_filter
        row.state_filter = payload.state_filter
        row.is_active = True
    db.commit()
    return {"ok": True, "subscribed": True}

@app.get("/api/corrigenda")
def list_recent_corrigenda(limit: int = 20, db: Session = Depends(get_db)):
    rows = db.query(CorrigendumLog).order_by(CorrigendumLog.detected_at.desc()).limit(min(limit, 50)).all()
    return [
        {
            "id": r.id,
            "vacancy_id": r.vacancy_id,
            "title": r.title,
            "field_changed": r.field_changed,
            "old_value": r.old_value,
            "new_value": r.new_value,
            "detected_at": r.detected_at.isoformat() if r.detected_at else None,
        }
        for r in rows
    ]
