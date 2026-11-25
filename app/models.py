import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text
from .database import Base

class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    organization = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)  # Central Govt, State PSC, NHM, Autonomous Institute, etc.
    state = Column(String(100), default="All India")
    designation = Column(String(255), nullable=False)
    qualification = Column(String(100), nullable=False)  # MBBS, MD/MS, BDS, AYUSH
    total_posts = Column(Integer, default=1)
    pay_scale = Column(String(100), nullable=True)
    last_date = Column(DateTime, nullable=True)
    notification_url = Column(Text, nullable=True)
    apply_url = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    
    # Eligibility & Criteria Parameters
    min_age = Column(Integer, default=21)
    max_age = Column(Integer, default=35)
    experience_years_required = Column(Integer, default=0)
    internship_must_complete = Column(Boolean, default=True)
    state_registration_mandatory = Column(Boolean, default=False)
    
    # Lifecycle Tracking
    stage = Column(String(50), default="APPLICATION_OPEN")  # APPLICATION_OPEN, ADMIT_CARD_OUT, EXAM_SCHEDULED, RESULTS_OUT
    exam_date = Column(DateTime, nullable=True)
    selection_mode = Column(String(100), default="Written Exam + Interview")  # Written CBT, Walk-in Interview, Merit
    
    # Bond & Service Terms (Critical for Doctors)
    bond_years = Column(Integer, default=0)
    bond_penalty_amount = Column(String(100), default="No Bond")
    
    # Category Distribution & Fees
    category_seats_json = Column(Text, nullable=True)  # JSON string: {"UR": 100, "OBC": 50, ...}
    application_fee = Column(String(100), default="As per rules")
    
    is_active = Column(Boolean, default=True)
    flag_count = Column(Integer, default=0)
    verification_status = Column(String(40), default="NEEDS_PDF_CHECK")  # VERIFIED_PDF, PORTAL_VERIFIED, NEEDS_PDF_CHECK
    memo_number = Column(String(120), nullable=True)
    last_verified_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel = Column(String(50), nullable=False)  # telegram, email, webhook
    target = Column(String(255), nullable=False)  # chat_id, email, url
    qualification_filter = Column(String(50), default="ALL")
    state_filter = Column(String(100), default="ALL")
    category_filter = Column(String(100), default="ALL")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vacancy_id = Column(String(36), nullable=False)
    channel = Column(String(50), nullable=False)
    target = Column(String(255), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="SUCCESS")
    details = Column(Text, nullable=True)

class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_id = Column(String(100), nullable=False)
    exam_title = Column(String(255), nullable=False)
    candidate_name = Column(String(120), nullable=False)
    final_score = Column(Float, nullable=False)
    correct = Column(Integer, default=0)
    wrong = Column(Integer, default=0)
    unattempted = Column(Integer, default=0)
    accuracy_pct = Column(Float, default=0.0)
    qualified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class PortalHealth(Base):
    __tablename__ = "portal_health"

    name = Column(String(100), primary_key=True)
    organization = Column(String(255), nullable=True)
    url = Column(Text, nullable=True)
    last_status = Column(Integer, nullable=True)
    latency_ms = Column(Integer, default=0)
    discovered_count = Column(Integer, default=0)
    consecutive_failures = Column(Integer, default=0)
    last_error = Column(Text, nullable=True)
    last_checked_at = Column(DateTime, default=datetime.utcnow)


class SyncJob(Base):
    __tablename__ = "sync_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(String(30), default="RUNNING")  # RUNNING, COMPLETED, FAILED
    portals_checked = Column(Integer, default=0)
    live_added = Column(Integer, default=0)
    sample_added = Column(Integer, default=0)
    error = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)


class RateLimitBucket(Base):
    __tablename__ = "rate_limit_buckets"

    key = Column(String(180), primary_key=True)
    timestamps_json = Column(Text, default="[]")
    updated_at = Column(DateTime, default=datetime.utcnow)


class SchemaMigration(Base):
    __tablename__ = "schema_migrations"

    version = Column(String(64), primary_key=True)
    applied_at = Column(DateTime, default=datetime.utcnow)


class DoctorSyncBlob(Base):
    __tablename__ = "doctor_sync_blobs"

    sync_key = Column(String(64), primary_key=True)
    payload_json = Column(Text, default="{}")
    updated_at = Column(DateTime, default=datetime.utcnow)


class PushSubscription(Base):
    __tablename__ = "push_subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    endpoint = Column(Text, nullable=False, unique=True)
    p256dh = Column(String(255), nullable=True)
    auth = Column(String(255), nullable=True)
    qualification_filter = Column(String(50), default="ALL")
    state_filter = Column(String(100), default="ALL")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class CorrigendumLog(Base):
    __tablename__ = "corrigendum_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vacancy_id = Column(String(36), nullable=False)
    title = Column(String(255), nullable=False)
    field_changed = Column(String(60), nullable=False)
    old_value = Column(String(120), nullable=True)
    new_value = Column(String(120), nullable=True)
    detected_at = Column(DateTime, default=datetime.utcnow)
