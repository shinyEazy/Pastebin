from datetime import datetime, timedelta
import logging
import pytz
from app.models.paste import Paste
from app.database import get_db
from app.redis import get_redis
import json

local_tz = pytz.timezone("Asia/Bangkok")

logging.basicConfig(
    filename="app.log", 
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

def is_expired(paste: Paste, total_views: int = None) -> bool:
    if paste.expiration == "Never":
        return False
    if paste.expiration == "Burn After Read":
        return total_views > 0 if total_views is not None else paste.views > 0
    
    expiration_map = {
        "1 Minute": timedelta(minutes=1), 
        "10 Minutes": timedelta(minutes=10),
        "1 Hour": timedelta(hours=1),
        "1 Day": timedelta(days=1),
        "1 Week": timedelta(weeks=1),
        "2 Weeks": timedelta(weeks=2),
        "1 Month": timedelta(days=30),
        "6 Months": timedelta(days=180),
        "1 Year": timedelta(days=365),
    }

    if paste.expiration in expiration_map:
        created_at_local = local_tz.localize(paste.created_at)  
        logging.info(f"Created at Local: {created_at_local}")
        
        expire_time = created_at_local + expiration_map[paste.expiration]
        logging.info(f"Expire time: {expire_time}")
        
        return datetime.now(local_tz) > expire_time

    return False

def update_paste_views():
    db = next(get_db())
    redis = next(get_redis())
    pastes_to_sync = redis.smembers("pastes_to_sync")

    for paste_id in pastes_to_sync:
        paste = db.query(Paste).filter(Paste.id == paste_id).first()
        if paste and paste.is_active:
            increment_key = f"paste:{paste_id}:views_increment"
            increment = int(redis.get(increment_key) or 0)
            
            if increment > 0:
                paste.views += increment
                db.commit()
                paste_key = f"paste:{paste_id}"
                cached_paste = redis.get(paste_key)
                if cached_paste:
                    paste_data = json.loads(cached_paste)
                    paste_data['views'] += increment
                    redis.set(paste_key, json.dumps(paste_data))
                    redis.expire(paste_key, 10)
                redis.set(increment_key, 0)
            redis.srem("pastes_to_sync", paste_id)
        else:
            logging.warning(f"Paste {paste_id} not found or inactive")