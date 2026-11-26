import os
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from .database import SessionLocal
from .collector import VacancyCollector
from .scraper import LiveGazetteScraper
from .notifier import Notifier
from .models import Vacancy

logger = logging.getLogger("medalerts.scheduler")
logging.basicConfig(level=logging.INFO)

scheduler = BackgroundScheduler()

def scheduled_recruitment_sync():
    """Runs periodic sync, live portal scraping, and T-48h closing alerts."""
    logger.info("Executing automated recruitment sync job...")
    db = SessionLocal()
    try:
        # 1. Sync curated & live gazette feeds
        sync_result = VacancyCollector.sync_sample_feed(db)
        live_result = LiveGazetteScraper.sync_live_portals(db)
        logger.info(f"Sync completed: Sample={sync_result}, Live={live_result}")

        # 2. Update expired vacancies & trigger T-48h closing alerts (evaluated in IST)
        now_ist = datetime.utcnow() + timedelta(hours=5, minutes=30)
        active_vacancies = db.query(Vacancy).filter(Vacancy.is_active == True).all()
        for v in active_vacancies:
            if v.stage in ("APPLICATION_CLOSED", "RESULTS_OUT", "INTERVIEW_OVER"):
                v.is_active = False
            elif v.last_date and v.last_date < now_ist:
                v.is_active = False
                v.stage = "APPLICATION_CLOSED"
                logger.info(f"Closed expired vacancy (deadline passed): {v.title}")
            elif v.exam_date and v.exam_date < now_ist:
                v.is_active = False
                v.stage = "INTERVIEW_OVER"
                logger.info(f"Closed vacancy (interview/exam date passed): {v.title}")
            elif not v.last_date and not v.exam_date and v.verification_status == "NEEDS_PDF_CHECK" and v.created_at and (v.created_at + timedelta(hours=5, minutes=30)) < now_ist - timedelta(days=7):
                v.is_active = False
                v.stage = "APPLICATION_CLOSED"
                logger.info(f"Closed stale undated vacancy (>7d): {v.title}")
            elif v.last_date and v.last_date <= now_ist + timedelta(hours=48):
                v.stage = "CLOSING_SOON"
                Notifier.broadcast_closing_reminder(db, v)
            elif v.last_date and v.last_date <= now_ist + timedelta(days=7):
                v.stage = "CLOSING_SOON"
        db.commit()
    except Exception as e:
        logger.error(f"Error during scheduled sync: {e}")
    finally:
        db.close()

def start_scheduler():
    if not scheduler.running:
        # Run every 6 hours by default
        poll_hours = int(os.getenv("POLL_INTERVAL_HOURS", 6))
        scheduler.add_job(
            scheduled_recruitment_sync,
            'interval',
            hours=poll_hours,
            id='recruitment_poller',
            replace_existing=True,
            next_run_time=datetime.now() + timedelta(minutes=10) # first background run in 10 mins
        )
        scheduler.start()
        logger.info(f"Background Scheduler started. Polling every {poll_hours} hours.")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Background Scheduler stopped.")
