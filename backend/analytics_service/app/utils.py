from shared.database import get_db
from shared.models.paste import Paste
from shared.redis import get_redis

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
                redis.set(increment_key, 0)
            redis.srem("pastes_to_sync", paste_id)