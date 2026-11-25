import os
import requests
from datetime import datetime
from sqlalchemy.orm import Session
from .models import Subscription, NotificationLog, Vacancy

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

class Notifier:
    @staticmethod
    def format_telegram_message(vacancy: Vacancy) -> str:
        last_date_str = vacancy.last_date.strftime("%d-%b-%Y") if vacancy.last_date else "Not Specified"
        exam_str = vacancy.exam_date.strftime("%d-%b-%Y") if vacancy.exam_date else "To be announced"
        
        msg = (
            f"🩺 <b>NEW MEDICAL OFFICER RECRUITMENT</b>\n\n"
            f"📌 <b>Title:</b> {vacancy.title}\n"
            f"🏥 <b>Organization:</b> {vacancy.organization}\n"
            f"🏛️ <b>Category:</b> {vacancy.category} ({vacancy.state})\n"
            f"🎯 <b>Status:</b> {vacancy.stage.replace('_', ' ').title()}\n"
            f"👥 <b>Total Posts:</b> {vacancy.total_posts} Seats\n"
            f"🎓 <b>Qualification:</b> {vacancy.qualification}\n"
            f"💰 <b>Pay Scale:</b> {vacancy.pay_scale or 'Level 10 Pay Matrix'}\n"
            f"📜 <b>Service Bond:</b> {vacancy.bond_penalty_amount or 'No Bond'}\n"
            f"📝 <b>Selection Mode:</b> {vacancy.selection_mode or 'Written Exam / Interview'}\n"
            f"📅 <b>Application Deadline:</b> {last_date_str}\n"
            f"🗓️ <b>Exam / Interview:</b> {exam_str}\n\n"
            f"🔗 <a href='{vacancy.notification_url or vacancy.apply_url or '#' }'>Official Gazette PDF</a> | "
            f"<a href='{vacancy.apply_url or vacancy.notification_url or '#' }'>Apply Portal</a>"
        )
        return msg

    @classmethod
    def send_to_subscription(cls, db: Session, sub: Subscription, vacancy: Vacancy) -> bool:
        if sub.qualification_filter != "ALL" and sub.qualification_filter.upper() not in vacancy.qualification.upper():
            return False
            
        if sub.state_filter != "ALL" and vacancy.state != "All India":
            allowed_states = [s.strip().upper() for s in sub.state_filter.split(",")]
            if vacancy.state.upper() not in allowed_states:
                return False

        if sub.category_filter != "ALL" and sub.category_filter.upper() not in vacancy.category.upper():
            return False

        status = "SUCCESS"
        details = ""

        if sub.channel == "telegram":
            if TELEGRAM_BOT_TOKEN:
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                try:
                    res = requests.post(
                        url,
                        json={
                            "chat_id": sub.target,
                            "text": cls.format_telegram_message(vacancy),
                            "parse_mode": "HTML",
                            "disable_web_page_preview": False
                        },
                        timeout=10
                    )
                    if not res.ok:
                        status = "FAILED"
                        details = f"Telegram API error: {res.text}"
                        if res.status_code in (400, 403) and ("chat not found" in res.text.lower() or "blocked" in res.text.lower()):
                            sub.is_active = False
                    else:
                        details = "Sent via Telegram Bot API"
                except Exception as e:
                    status = "FAILED"
                    details = str(e)
            else:
                details = "Simulated delivery (Set TELEGRAM_BOT_TOKEN to enable real Telegram dispatches)"

        elif sub.channel == "webhook":
            try:
                res = requests.post(
                    sub.target,
                    json={
                        "event": "NEW_VACANCY",
                        "vacancy": {
                            "id": vacancy.id,
                            "title": vacancy.title,
                            "organization": vacancy.organization,
                            "qualification": vacancy.qualification,
                            "total_posts": vacancy.total_posts,
                            "stage": vacancy.stage,
                            "bond": vacancy.bond_penalty_amount,
                            "last_date": vacancy.last_date.isoformat() if vacancy.last_date else None,
                            "apply_url": vacancy.apply_url
                        }
                    },
                    timeout=5
                )
                if not res.ok:
                    status = "FAILED"
                    details = f"Webhook HTTP {res.status_code}"
                else:
                    details = f"Webhook HTTP {res.status_code}"
            except Exception as e:
                status = "FAILED"
                details = str(e)

        elif sub.channel == "email":
            details = f"Simulated email notification dispatched to {sub.target}"

        log = NotificationLog(
            vacancy_id=vacancy.id,
            channel=sub.channel,
            target=sub.target,
            sent_at=datetime.utcnow(),
            status=status,
            details=details
        )
        db.add(log)
        db.commit()
        return status == "SUCCESS"

    @classmethod
    def broadcast_new_vacancy(cls, db: Session, vacancy: Vacancy) -> int:
        subscriptions = db.query(Subscription).filter(Subscription.is_active == True).all()
        sent_count = 0
        for sub in subscriptions:
            if cls.send_to_subscription(db, sub, vacancy):
                sent_count += 1
        return sent_count

    @classmethod
    def broadcast_closing_reminder(cls, db: Session, vacancy: Vacancy) -> int:
        """Sends a one-time T-48h closing-soon reminder to active Telegram subscribers."""
        already_reminded = db.query(NotificationLog).filter(
            NotificationLog.vacancy_id == vacancy.id,
            NotificationLog.details.like("%CLOSING_48H%")
        ).first()
        if already_reminded:
            return 0

        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        subscriptions = db.query(Subscription).filter(
            Subscription.is_active == True,
            Subscription.channel == "telegram"
        ).all()

        sent = 0
        due_str = vacancy.last_date.strftime("%d %b %Y") if vacancy.last_date else "Soon"
        msg = (
            f"⏰ <b>CLOSING IN 48 HOURS</b>\n\n"
            f"📌 <b>{vacancy.title}</b>\n"
            f"🏢 {vacancy.organization} ({vacancy.state})\n"
            f"👥 <b>Seats:</b> {vacancy.total_posts} | 🎓 <b>Qual:</b> {vacancy.qualification}\n"
            f"📅 <b>Deadline:</b> {due_str}\n\n"
            f"🔗 <a href='{vacancy.apply_url or 'https://medalerts.onrender.com'}'>Apply Before Portal Closes</a>"
        )

        for sub in subscriptions:
            status = "SUCCESS"
            details = "CLOSING_48H reminder logged"
            if bot_token:
                try:
                    res = requests.post(
                        f"https://api.telegram.org/bot{bot_token}/sendMessage",
                        json={"chat_id": sub.target, "text": msg, "parse_mode": "HTML"},
                        timeout=6
                    )
                    if res.ok:
                        details = "CLOSING_48H Telegram reminder sent"
                        sent += 1
                    else:
                        status = "FAILED"
                        details = f"CLOSING_48H HTTP {res.status_code}"
                except Exception as e:
                    status = "FAILED"
                    details = f"CLOSING_48H err: {e}"
            db.add(NotificationLog(
                vacancy_id=vacancy.id,
                channel="telegram",
                target=sub.target,
                sent_at=datetime.utcnow(),
                status=status,
                details=details
            ))
            db.commit()
        return sent
