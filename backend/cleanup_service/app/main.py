from apscheduler.schedulers.blocking import BlockingScheduler
from app.utils import cleanup_expired_pastes
from shared.models.user import User
from shared.models.paste import Paste 

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(cleanup_expired_pastes, 'interval', hours=1)
    scheduler.start()