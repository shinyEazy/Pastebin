from apscheduler.schedulers.background import BackgroundScheduler
from app.utils import update_paste_views

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        update_paste_views,
        'interval',
        seconds=30
    )
    scheduler.start()