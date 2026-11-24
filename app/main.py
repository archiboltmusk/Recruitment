import os
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import FastAPI, Depends, Query, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from .database import engine, Base, get_db
from .models import Vacancy, Subscription, NotificationLog
from .collector import VacancyCollector
from .notifier import Notifier

# Initialize database schema
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MedAlerts - Medical Officer Vacancies Aggregator",
    description="Unified API & notification engine for Medical Officer posts across UPSC, State PSCs, NHM, and AIIMS.",
    version="1.0.0"
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
    pay_scale: Optional[str] = None
    last_date: Optional[datetime] = None
    notification_url: Optional[str] = None
    apply_url: Optional[str] = None
    summary: Optional[str] = None

class SubscriptionCreate(BaseModel):
    channel: str = Field(..., description="telegram, email, or webhook")
    target: str = Field(..., description="Telegram Chat ID, Email Address, or Webhook URL")
    qualification_filter: str = "ALL"
    state_filter: str = "ALL"
    category_filter: str = "ALL"

# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.on_event("startup")
def on_startup():
    # Automatically seed sample vacancies if DB is empty
    from .database import SessionLocal
    db = SessionLocal()
    try:
        count = db.query(Vacancy).count()
        if count == 0:
            VacancyCollector.sync_sample_feed(db)
    finally:
        db.close()

@app.get("/")
def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "MedAlerts API is live. Visit /docs for the API Swagger."}

@app.get("/api/stats")
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
        "active_subscribers": subscribers_count
    }

@app.get("/api/vacancies")
def list_vacancies(
    search: Optional[str] = None,
    qualification: Optional[str] = None,
    category: Optional[str] = None,
    state: Optional[str] = None,
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

    # Order by nearest deadline first
    vacancies = query.order_by(Vacancy.last_date.asc()).all()

    # Calculate days left for each
    results = []
    now = datetime.utcnow()
    for v in vacancies:
        days_left = None
        if v.last_date:
            delta = (v.last_date - now).total_seconds() / 86400.0
            days_left = max(0, int(delta))

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
            "last_date": v.last_date.strftime("%Y-%m-%d") if v.last_date else None,
            "days_left": days_left,
            "notification_url": v.notification_url,
            "apply_url": v.apply_url,
            "summary": v.summary,
            "created_at": v.created_at.strftime("%Y-%m-%d") if v.created_at else None
        })

    return results

@app.post("/api/vacancies", status_code=status.HTTP_201_CREATED)
def create_vacancy(payload: VacancyCreate, db: Session = Depends(get_db)):
    vacancy = VacancyCollector.parse_and_add_custom(db, payload.dict())
    return {"message": "Vacancy added and broadcast dispatched", "id": vacancy.id}

@app.post("/api/collector/refresh")
def refresh_collector(db: Session = Depends(get_db)):
    result = VacancyCollector.sync_sample_feed(db)
    return {"message": "Recruitment aggregator executed successfully", **result}

@app.post("/api/subscriptions", status_code=status.HTTP_201_CREATED)
def subscribe(payload: SubscriptionCreate, db: Session = Depends(get_db)):
    # Check if existing
    existing = db.query(Subscription).filter(
        Subscription.channel == payload.channel,
        Subscription.target == payload.target
    ).first()

    if existing:
        existing.qualification_filter = payload.qualification_filter
        existing.state_filter = payload.state_filter
        existing.category_filter = payload.category_filter
        existing.is_active = True
        db.commit()
        return {"message": "Subscription updated successfully", "id": existing.id}

    sub = Subscription(
        channel=payload.channel.lower(),
        target=payload.target,
        qualification_filter=payload.qualification_filter,
        state_filter=payload.state_filter,
        category_filter=payload.category_filter,
        is_active=True
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return {"message": f"Successfully subscribed to {sub.channel} alerts", "id": sub.id}

@app.get("/api/subscriptions")
def list_subscriptions(db: Session = Depends(get_db)):
    return db.query(Subscription).all()

@app.get("/api/notifications/recent")
def list_notifications(limit: int = 15, db: Session = Depends(get_db)):
    logs = db.query(NotificationLog).order_by(NotificationLog.sent_at.desc()).limit(limit).all()
    return logs
