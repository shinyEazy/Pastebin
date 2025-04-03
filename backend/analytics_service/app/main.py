from apscheduler.schedulers.blocking import BlockingScheduler
from app.utils import update_paste_views

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(update_paste_views, 'interval', seconds=60)
    scheduler.start()