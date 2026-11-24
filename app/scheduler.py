import os
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from .database import SessionLocal
from .collector import VacancyCollector
from .models import Vacancy

logger = logging.getLogger("medalerts.scheduler")
logging.basicConfig(level=logging.INFO)

scheduler = BackgroundScheduler()

def scheduled_recruitment_sync():
    """Runs periodic sync and updates lifecycle statuses."""
    logger.info("Executing automated recruitment sync job...")
    db = SessionLocal()
    try:
        # 1. Sync feeds
        sync_result = VacancyCollector.sync_sample_feed(db)
        logger.info(f"Sync completed: Added={sync_result['added']}, Updated={sync_result['updated']}")

        # 2. Update expired vacancies & stages
        now = datetime.utcnow()
        active_vacancies = db.query(Vacancy).filter(Vacancy.is_active == True).all()
        for v in active_vacancies:
            if v.last_date and v.last_date < now:
                v.is_active = False
                v.stage = "APPLICATION_CLOSED"
                logger.info(f"Closed expired vacancy: {v.title}")
            elif v.last_date and v.last_date <= now + timedelta(days=3):
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
