import os
import smtplib
from email.mime.text import MIMEText
import requests
from datetime import datetime, timedelta
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
            ok, info = cls.send_email_alert(
                to_email=sub.target,
                subject=f"MedAlerts: {vacancy.title} ({vacancy.total_posts} Seats)",
                html_body=f"""
                <h3>{vacancy.title}</h3>
                <p><strong>Organization:</strong> {vacancy.organization} ({vacancy.state})</p>
                <p><strong>Qualification:</strong> {vacancy.qualification} | <strong>Seats:</strong> {vacancy.total_posts}</p>
                <p><strong>Bond:</strong> {vacancy.bond_penalty_amount or 'No Bond'}</p>
                <p><strong>Deadline:</strong> {vacancy.last_date.strftime('%d-%b-%Y') if vacancy.last_date else 'Check Notice'}</p>
                <p><a href="{vacancy.apply_url or 'https://medalerts.onrender.com'}">Apply on Official Portal</a></p>
                """
            )
            if not ok:
                status = "FAILED"
            details = info

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

    @staticmethod
    def send_email_alert(to_email: str, subject: str, html_body: str):
        """Sends email via Resend API or SMTP if configured; falls back gracefully to simulated log."""
        resend_key = os.getenv("RESEND_API_KEY", "").strip()
        if resend_key:
            try:
                from_addr = os.getenv("RESEND_FROM_EMAIL", "MedAlerts <alerts@resend.dev>")
                res = requests.post(
                    "https://api.resend.com/emails",
                    headers={"Authorization": f"Bearer {resend_key}", "Content-Type": "application/json"},
                    json={"from": from_addr, "to": [to_email], "subject": subject, "html": html_body},
                    timeout=10
                )
                if res.ok:
                    return True, f"Sent via Resend API to {to_email}"
                return False, f"Resend HTTP {res.status_code}: {res.text[:120]}"
            except Exception as e:
                return False, f"Resend error: {e}"

        smtp_host = os.getenv("SMTP_HOST", "").strip()
        smtp_user = os.getenv("SMTP_USER", "").strip()
        smtp_pass = os.getenv("SMTP_PASS", "").strip()
        if smtp_host and smtp_user and smtp_pass:
            try:
                smtp_port = int(os.getenv("SMTP_PORT", "587"))
                msg = MIMEText(html_body, "html")
                msg["Subject"] = subject
                msg["From"] = smtp_user
                msg["To"] = to_email
                with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_pass)
                    server.sendmail(smtp_user, [to_email], msg.as_string())
                return True, f"Sent via SMTP to {to_email}"
            except Exception as e:
                return False, f"SMTP error: {e}"

        return True, f"Simulated email (configure RESEND_API_KEY or SMTP_* for live emails)"

    @classmethod
    def broadcast_daily_digest(cls, db: Session, target_channel: str = None) -> dict:
        """Dispatches a curated morning briefing of active & closing-soon circulars to Telegram."""
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        if not bot_token:
            return {"sent": 0, "reason": "TELEGRAM_BOT_TOKEN not set"}

        active = db.query(Vacancy).filter(Vacancy.is_active == True).all()
        total_seats = sum(v.total_posts for v in active)
        now = datetime.utcnow()
        closing_soon = [v for v in active if v.last_date and (v.last_date - now).days <= 7]
        walkins = [v for v in active if v.selection_mode and "walk-in" in v.selection_mode.lower()]

        lines = [
            f"🩺 <b>MEDALERTS MORNING BRIEFING</b>",
            f"📊 <b>{len(active)} Active Circulars</b> | <b>{total_seats:,} Open Seats</b>\n"
        ]
        if closing_soon:
            lines.append("⏰ <b>Closing Within 7 Days:</b>")
            for v in closing_soon[:4]:
                days = max(0, (v.last_date - now).days) if v.last_date else 0
                lines.append(f"• <b>{v.title}</b> ({v.total_posts} seats) — <i>{days}d left</i>")
            lines.append("")
        if walkins:
            lines.append("🚶 <b>Zero-Exam Walk-in Interviews:</b>")
            for v in walkins[:4]:
                lines.append(f"• <b>{v.title}</b> ({v.state}) — {v.total_posts} seats")
            lines.append("")
        lines.append("🔗 <a href='https://medalerts.onrender.com'>Open MedAlerts Dashboard</a> | <a href='https://medalerts.onrender.com/onboarding'>Check Eligibility</a>")

        digest_text = "\n".join(lines)
        targets = [target_channel] if target_channel else [
            s.target for s in db.query(Subscription).filter(
                Subscription.is_active == True,
                Subscription.channel == "telegram"
            ).all()
        ]
        if not targets:
            targets = [os.getenv("TELEGRAM_DEFAULT_CHANNEL", "@MedAlerts_Official")]

        sent = 0
        for chat_id in set(targets):
            try:
                res = requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": chat_id, "text": digest_text, "parse_mode": "HTML"},
                    timeout=10
                )
                if res.ok:
                    sent += 1
            except Exception:
                pass
        return {"sent": sent, "targets": len(set(targets))}
