from sqlalchemy.orm import Session
from shared.models.paste import Paste
from shared.utils import is_expired
from shared.schemas import paste
import json
from shared.models.user import User
import time
import threading
import queue
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

paste_queue = queue.Queue()
last_batch_execution = time.time()
batch_lock = threading.Lock()

MAX_BATCH_SIZE = 1000
BATCH_INTERVAL = 5

def batch_worker():
    """Background worker thread that processes the paste queue."""
    global last_batch_execution
    
    while True:
        current_time = time.time()
        should_process = False
        
        with batch_lock:
            queue_size = paste_queue.qsize()
            time_elapsed = current_time - last_batch_execution
            
            if queue_size >= MAX_BATCH_SIZE or (queue_size > 0 and time_elapsed >= BATCH_INTERVAL):
                should_process = True
                
        if should_process:
            process_batch()
            with batch_lock:
                last_batch_execution = time.time()
        
        time.sleep(0.5)

def process_batch():
    """Process accumulated paste records in batch."""
    from shared.database import get_db
    
    batch_items = []
    batch_redis_updates = []
    
    try:
        db = next(get_db())
        
        queue_size = min(paste_queue.qsize(), MAX_BATCH_SIZE)
        for _ in range(queue_size):
            if not paste_queue.empty():
                item = paste_queue.get_nowait()
                batch_items.append(item["paste_obj"])
                batch_redis_updates.append(item)
        
        if not batch_items:
            return
            
        db.add_all(batch_items)
        db.commit()
        
        for i, paste_obj in enumerate(batch_items):
            db.refresh(paste_obj)
            item = batch_redis_updates[i]
            
            paste_schema = paste.Paste.from_orm(paste_obj)
            paste_key = f"paste:{paste_obj.id}"
            item["redis"].set(paste_key, paste_schema.json())
            item["redis"].expire(paste_key, 1800)
            
            if "callback" in item and item["callback"]:
                item["callback"](paste_schema)
                
        logger.info(f"Successfully processed batch of {len(batch_items)} pastes")
            
    except Exception as e:
        logger.error(f"Error processing batch: {str(e)}")
        try:
            db.rollback()
        except:
            pass
        
        for item in batch_redis_updates:
            paste_queue.put(item)
    finally:
        db.close()

batch_thread = threading.Thread(target=batch_worker, daemon=True)
batch_thread.start()

def create_paste(db: Session, paste_data: paste.PasteCreate, redis, current_user: User = None, sync=False):
    """
    Create a new paste record.
    
    Args:
        db: Database session
        paste_data: Paste data
        redis: Redis connection
        current_user: Current authenticated user (optional)
        sync: If True, process immediately instead of batching (default: False)
    
    Returns:
        paste_schema: Created paste schema
    """
    db_paste = Paste(
        **paste_data.dict(),
        user_id=current_user.id if current_user else None
    )
    
    if sync:
        db.commit()
        db.refresh(db_paste)
        paste_schema = paste.Paste.from_orm(db_paste)
        paste_key = f"paste:{db_paste.id}"
        redis.set(paste_key, paste_schema.json())
        redis.expire(paste_key, 1800)
        return paste_schema
    else:
        result_queue = queue.Queue(1)
        
        def set_result(result):
            result_queue.put(result)
        
        paste_queue.put({
            "paste_obj": db_paste,
            "redis": redis,
            "callback": set_result
        })
        
        try:
            return result_queue.get(timeout=10)
        except queue.Empty:
            logger.warning("Batch processing timeout, falling back to sync processing")
            return create_paste(db, paste_data, redis, current_user, sync=True)

def get_paste(db: Session, paste_id: str, redis):
    paste_key = f"paste:{paste_id}"
    increment_key = f"paste:{paste_id}:views_increment"
    cached_paste = redis.get(paste_key)
    if cached_paste:
        paste_schema = paste.Paste.parse_raw(cached_paste)
        redis.expire(paste_key, 1800)
    else:
        db_paste = db.query(Paste).filter(Paste.id == paste_id).first()
        if not db_paste or not db_paste.is_active:
            return None
        paste_schema = paste.Paste.from_orm(db_paste)
        redis.set(paste_key, paste_schema.json())
        redis.expire(paste_key, 1800)

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