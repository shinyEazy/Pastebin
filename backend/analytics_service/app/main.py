from apscheduler.schedulers.blocking import BlockingScheduler
from app.utils import update_paste_views
from shared.models.user import User
from shared.models.paste import Paste

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(update_paste_views, 'interval', minutes=5)
    scheduler.start()