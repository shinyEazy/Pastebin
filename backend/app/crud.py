from sqlalchemy.orm import Session
from app.models.paste import Paste
from app.utils import is_expired
from app import schemas

def create_paste(db: Session, paste: schemas.PasteCreate, redis):
    db_paste = Paste(**paste.dict())
    db.add(db_paste)
    db.commit()
    db.refresh(db_paste)
    paste_schema = schemas.Paste.from_orm(db_paste)
    paste_key = f"paste:{db_paste.id}"
    redis.set(paste_key, paste_schema.json())
    redis.expire(paste_key, 10)
    return paste_schema

def get_paste(db, paste_id: str, redis):
    paste_key = f"paste:{paste_id}"
    increment_key = f"paste:{paste_id}:views_increment"
    cached_paste = redis.get(paste_key)
    if cached_paste:
        paste_schema = schemas.Paste.parse_raw(cached_paste)
        redis.expire(paste_key, 10)
    else:
        paste = db.query(Paste).filter(Paste.id == paste_id).first()
        if not paste or not paste.is_active:
            return None
        paste_schema = schemas.Paste.from_orm(paste)
        redis.set(paste_key, paste_schema.json())
        redis.expire(paste_key, 10)
    
    increment = int(redis.get(increment_key) or 0)
    total_views = paste_schema.views + increment
    
    if is_expired(paste_schema, total_views=total_views):
        db.query(Paste).filter(Paste.id == paste_id).update({
            "views": total_views,
            "is_active": False
        })
        db.commit()
        redis.delete(paste_key)
        redis.delete(increment_key)
        redis.srem("pastes_to_sync", paste_id)
        return None
    
    redis.incr(increment_key)
    redis.sadd("pastes_to_sync", paste_id)
    
    paste_schema.views = total_views + 1
    return paste_schema