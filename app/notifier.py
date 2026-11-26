import os
import json
import hmac
import hashlib
import html
import smtplib
from email.mime.text import MIMEText
import requests
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models import Subscription, NotificationLog, Vacancy, PushSubscription
from .pdf_parser import GovtNotificationPDFParser

try:
    from pywebpush import webpush, WebPushException
except ImportError:
    webpush = None
    WebPushException = Exception

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
APP_BASE_URL = os.getenv("APP_BASE_URL", "https://medalerts.onrender.com").rstrip("/")

class Notifier:
    @staticmethod
    def format_telegram_message(vacancy: Vacancy) -> str:
        last_date_str = vacancy.last_date.strftime("%d-%b-%Y") if vacancy.last_date else "Not Specified"
        exam_str = vacancy.exam_date.strftime("%d-%b-%Y") if vacancy.exam_date else "To be announced"
        esc = lambda s: html.escape(str(s or ""))
        notif_url = esc(vacancy.notification_url or vacancy.apply_url or "#")
        apply_url = esc(vacancy.apply_url or vacancy.notification_url or "#")
        
        msg = (
            f"🩺 <b>NEW MEDICAL OFFICER RECRUITMENT</b>\n\n"
            f"📌 <b>Title:</b> {esc(vacancy.title)}\n"
            f"🏥 <b>Organization:</b> {esc(vacancy.organization)}\n"
            f"🏛️ <b>Category:</b> {esc(vacancy.category)} ({esc(vacancy.state)})\n"
            f"🎯 <b>Status:</b> {esc((vacancy.stage or '').replace('_', ' ').title())}\n"
            f"👥 <b>Total Posts:</b> {vacancy.total_posts or 0} Seats\n"
            f"🎓 <b>Qualification:</b> {esc(vacancy.qualification)}\n"
            f"💰 <b>Pay Scale:</b> {esc(vacancy.pay_scale or 'Level 10 Pay Matrix')}\n"
            f"📜 <b>Service Bond:</b> {esc(vacancy.bond_penalty_amount or 'No Bond')}\n"
            f"📝 <b>Selection Mode:</b> {esc(vacancy.selection_mode or 'Written Exam / Interview')}\n"
            f"📅 <b>Application Deadline:</b> {last_date_str}\n"
            f"🗓️ <b>Exam / Interview:</b> {exam_str}\n\n"
            f"🔗 <a href='{notif_url}'>Official Gazette PDF</a> | "
            f"<a href='{apply_url}'>Apply Portal</a>"
        )
        return msg

    @staticmethod
    def _matches_subscription(sub: Subscription, vacancy: Vacancy) -> bool:
        if sub.qualification_filter and sub.qualification_filter != "ALL":
            if sub.qualification_filter.upper() not in (vacancy.qualification or "").upper():
                return False
        if sub.state_filter and sub.state_filter != "ALL" and (vacancy.state or "") != "All India":
            allowed_states = [s.strip().upper() for s in sub.state_filter.split(",") if s.strip()]
            if allowed_states and (vacancy.state or "").upper() not in allowed_states:
                return False
        if sub.category_filter and sub.category_filter != "ALL":
            if sub.category_filter.upper() not in (vacancy.category or "").upper():
                return False
        if getattr(sub, "zero_bond_only", False) and (vacancy.bond_years or 0) > 0:
            return False
        return True

    @classmethod
    def send_to_subscription(cls, db: Session, sub: Subscription, vacancy: Vacancy) -> bool:
        if not cls._matches_subscription(sub, vacancy):
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
            if not GovtNotificationPDFParser.is_safe_url(sub.target):
                status = "FAILED"
                details = "Blocked unsafe or private webhook URL"
            else:
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
                        timeout=5,
                        allow_redirects=False
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
            esc = lambda s: html.escape(str(s or ""))
            sec = (os.getenv("ADMIN_API_KEY") or os.getenv("TELEGRAM_BOT_TOKEN") or "").encode("utf-8")
            unsub_html = ""
            if sec:
                tok = hmac.new(sec, f"{sub.id}:{sub.target}".encode("utf-8"), hashlib.sha256).hexdigest()[:24]
                unsub_url = f"{APP_BASE_URL}/api/unsubscribe?id={sub.id}&token={tok}"
                unsub_html = f"<p style='font-size:11px;color:#666'><a href='{esc(unsub_url)}'>Unsubscribe</a></p>"
            ok, info = cls.send_email_alert(
                to_email=sub.target,
                subject=f"MedAlerts: {vacancy.title} ({vacancy.total_posts} Seats)",
                html_body=f"""
                <h3>{esc(vacancy.title)}</h3>
                <p><strong>Organization:</strong> {esc(vacancy.organization)} ({esc(vacancy.state)})</p>
                <p><strong>Qualification:</strong> {esc(vacancy.qualification)} | <strong>Seats:</strong> {vacancy.total_posts}</p>
                <p><strong>Bond:</strong> {esc(vacancy.bond_penalty_amount or 'No Bond')}</p>
                <p><strong>Deadline:</strong> {vacancy.last_date.strftime('%d-%b-%Y') if vacancy.last_date else 'Check Notice'}</p>
                <p><a href="{esc(vacancy.apply_url or APP_BASE_URL)}">Apply on Official Portal</a></p>
                {unsub_html}
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
    def broadcast_web_push(cls, db: Session, vacancy: Vacancy) -> int:
        priv_key = os.getenv('VAPID_PRIVATE_KEY', '').strip()
        if not (webpush and priv_key):
            return 0
        claims_sub = os.getenv('VAPID_CLAIMS_SUB', 'mailto:alerts@medalerts.onrender.com').strip()
        subs = db.query(PushSubscription).filter(PushSubscription.is_active == True).all()
        payload = json.dumps({
            'title': f'MedAlerts: {(vacancy.title or "")[:80]}',
            'body': f'{vacancy.organization} ({vacancy.state}) - {vacancy.total_posts or "Check"} Seats',
            'url': f'{APP_BASE_URL}/?job={vacancy.id}',
        })
        sent = 0
        for ps in subs:
            if ps.qualification_filter and ps.qualification_filter != 'ALL':
                if ps.qualification_filter.upper() not in (vacancy.qualification or '').upper():
                    continue
            if ps.state_filter and ps.state_filter != 'ALL' and (vacancy.state or '') != 'All India':
                if ps.state_filter.upper() != (vacancy.state or '').upper():
                    continue
            if not (ps.p256dh and ps.auth):
                continue
            try:
                webpush(
                    subscription_info={'endpoint': ps.endpoint, 'keys': {'p256dh': ps.p256dh, 'auth': ps.auth}},
                    data=payload,
                    vapid_private_key=priv_key,
                    vapid_claims={'sub': claims_sub},
                    timeout=5,
                )
                sent += 1
            except WebPushException as exc:
                resp = getattr(exc, 'response', None)
                if resp is not None and getattr(resp, 'status_code', None) in (404, 410):
                    ps.is_active = False
            except Exception:
                pass
        if subs:
            db.commit()
        return sent

    @classmethod
    def broadcast_new_vacancy(cls, db: Session, vacancy: Vacancy) -> int:
        subscriptions = db.query(Subscription).filter(Subscription.is_active == True).all()
        sent_count = 0
        for sub in subscriptions:
            if cls.send_to_subscription(db, sub, vacancy):
                sent_count += 1
        cls.broadcast_web_push(db, vacancy)
        return sent_count

    @classmethod
    def broadcast_corrigendum(cls, db: Session, vacancy: Vacancy, changes: list) -> int:
        if not changes:
            return 0
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        subs = db.query(Subscription).filter(Subscription.is_active == True, Subscription.channel == "telegram").all()
        esc = lambda s: html.escape(str(s or ""))
        change_lines = "\n".join(f"• <b>{esc(c['field'])}:</b> {esc(c['old'])} → {esc(c['new'])}" for c in changes)
        msg = (
            f"📢 <b>CORRIGENDUM / DEADLINE UPDATE</b>\n\n"
            f"📌 <b>{esc(vacancy.title)}</b>\n"
            f"🏥 {esc(vacancy.organization)}\n"
            f"{change_lines}\n\n"
            f"🔗 <a href='{esc(vacancy.apply_url or APP_BASE_URL)}'>View Circular</a>"
        )
        sent = 0
        for sub in subs:
            if not cls._matches_subscription(sub, vacancy):
                continue
            status = "SUCCESS"
            details = "Corrigendum logged"
            if bot_token:
                try:
                    res = requests.post(
                        f"https://api.telegram.org/bot{bot_token}/sendMessage",
                        json={"chat_id": sub.target, "text": msg, "parse_mode": "HTML"},
                        timeout=6,
                    )
                    if res.ok:
                        details = "Corrigendum Telegram alert sent"
                        sent += 1
                    else:
                        status = "FAILED"
                        details = f"Corrigendum HTTP {res.status_code}"
                except Exception as e:
                    status = "FAILED"
                    details = f"Corrigendum err: {e}"
            db.add(NotificationLog(
                vacancy_id=vacancy.id,
                channel="telegram",
                target=sub.target,
                sent_at=datetime.utcnow(),
                status=status,
                details=details,
            ))
            db.commit()
        return sent

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
        esc = lambda s: html.escape(str(s or ""))
        msg = (
            f"⏰ <b>CLOSING IN 48 HOURS</b>\n\n"
            f"📌 <b>{esc(vacancy.title)}</b>\n"
            f"🏢 {esc(vacancy.organization)} ({esc(vacancy.state)})\n"
            f"👥 <b>Seats:</b> {vacancy.total_posts} | 🎓 <b>Qual:</b> {esc(vacancy.qualification)}\n"
            f"📅 <b>Deadline:</b> {due_str}\n\n"
            f"🔗 <a href='{esc(vacancy.apply_url or APP_BASE_URL)}'>Apply Before Portal Closes</a>"
        )

        for sub in subscriptions:
            if not cls._matches_subscription(sub, vacancy):
                continue
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
    def broadcast_daily_digest(cls, db: Session, target_channel: str = None, force: bool = False) -> dict:
        """Dispatches a curated morning briefing of active & closing-soon circulars to Telegram (once per UTC day unless forced)."""
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        if not bot_token:
            return {"sent": 0, "reason": "TELEGRAM_BOT_TOKEN not set"}

        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        if not force:
            already_sent = db.query(NotificationLog).filter(
                NotificationLog.vacancy_id == "DAILY_DIGEST",
                NotificationLog.status == "SUCCESS",
                NotificationLog.sent_at >= today_start
            ).first()
            if already_sent:
                return {"sent": 0, "skipped": True, "reason": "Daily digest already sent today"}

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
                lines.append(f"• <b>{html.escape(v.title or '')}</b> ({v.total_posts} seats) — <i>{days}d left</i>")
            lines.append("")
        if walkins:
            lines.append("🚶 <b>Zero-Exam Walk-in Interviews:</b>")
            for v in walkins[:4]:
                lines.append(f"• <b>{html.escape(v.title or '')}</b> ({html.escape(v.state or '')}) — {v.total_posts} seats")
            lines.append("")
        lines.append(f"🔗 <a href='{APP_BASE_URL}'>Open MedAlerts Dashboard</a> | <a href='{APP_BASE_URL}/onboarding'>Check Eligibility</a>")

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
                    db.add(NotificationLog(
                        vacancy_id="DAILY_DIGEST",
                        channel="telegram",
                        target=chat_id,
                        sent_at=datetime.utcnow(),
                        status="SUCCESS",
                        details="Daily morning briefing sent"
                    ))
                    db.commit()
            except Exception:
                pass
        return {"sent": sent, "targets": len(set(targets))}

    @classmethod
    def handle_telegram_command(cls, db: Session, chat_id: str, text: str) -> str:
        """Handles interactive Telegram bot commands (/start, /filter, /closing, /stop)."""
        cmd_raw = (text or "").strip()
        parts = cmd_raw.split()
        cmd = parts[0].lower().split("@")[0] if parts else ""
        chat_id_str = str(chat_id).strip()

        sub = db.query(Subscription).filter(
            Subscription.channel == "telegram",
            Subscription.target == chat_id_str,
        ).first()

        if cmd == "/start":
            if not sub:
                sub = Subscription(
                    channel="telegram",
                    target=chat_id_str,
                    qualification_filter="ALL",
                    state_filter="ALL",
                    category_filter="ALL",
                    is_active=True,
                )
                db.add(sub)
            else:
                sub.is_active = True
            db.commit()
            return (
                "🩺 <b>Welcome to MedAlerts Bot!</b>\n"
                "You're subscribed to live Medical Officer recruitment alerts.\n\n"
                "<b>Commands:</b>\n"
                "• <code>/filter MBBS WestBengal</code> — Set degree &amp; state filter\n"
                "• <code>/closing</code> — View notices closing soon\n"
                "• <code>/stop</code> — Pause alerts"
            )

        if cmd == "/filter":
            qual = parts[1].upper() if len(parts) > 1 else "ALL"
            if qual not in ("ALL", "MBBS", "MD/MS", "AYUSH"):
                qual = "MBBS" if "MBBS" in qual else ("MD/MS" if "MD" in qual or "MS" in qual or "PG" in qual else "ALL")
            state = " ".join(parts[2:]).strip() if len(parts) > 2 else "ALL"
            if state.lower() in ("wb", "westbengal", "west_bengal"):
                state = "West Bengal"
            elif state.lower() in ("allindia", "all_india", "india"):
                state = "All India"
            if not sub:
                sub = Subscription(channel="telegram", target=chat_id_str, is_active=True)
                db.add(sub)
            sub.qualification_filter = qual
            sub.state_filter = state or "ALL"
            sub.is_active = True
            db.commit()
            return f"✅ Filter updated: <b>{html.escape(qual)}</b> | State: <b>{html.escape(sub.state_filter)}</b>"

        if cmd == "/closing":
            rows = (
                db.query(Vacancy)
                .filter(Vacancy.is_active == True)
                .order_by(Vacancy.last_date.asc())
                .limit(5)
                .all()
            )
            if not rows:
                return "No active notices found right now."
            lines = ["⏰ <b>Top Active / Closing Notices:</b>"]
            for v in rows:
                due = v.last_date.strftime("%d %b %Y") if v.last_date else "Check PDF"
                lines.append(f"• <b>{html.escape(v.title or '')}</b> ({v.total_posts or 0} seats) — Due: {due}")
            lines.append(f"\n🔗 <a href='{APP_BASE_URL}'>Open MedAlerts</a>")
            return "\n".join(lines)

        if cmd == "/stop":
            if sub:
                sub.is_active = False
                db.commit()
            return "⏸️ Alerts paused. Send /start anytime to resume."

        return (
            "Available commands:\n"
            "• <code>/start</code> — Subscribe\n"
            "• <code>/filter MBBS WestBengal</code> — Filter alerts\n"
            "• <code>/closing</code> — Closing soon\n"
            "• <code>/stop</code> — Pause alerts"
        )
