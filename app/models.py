import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text
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
    is_active = Column(Boolean, default=True)
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
