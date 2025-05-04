import threading
import queue
import time
import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from shared.models.paste import Paste
from shared.schemas import paste
from shared.utils import is_expired

logger = logging.getLogger(__name__)

# Configure multiple worker threads for better throughput
NUM_WORKER_THREADS = 4
MAX_BATCH_SIZE = 500  # Smaller batch size for more frequent processing
BATCH_INTERVAL = 3    # Process more frequently

paste_queues = [queue.Queue() for _ in range(NUM_WORKER_THREADS)]
batch_locks = [threading.Lock() for _ in range(NUM_WORKER_THREADS)]
last_batch_executions = [time.time() for _ in range(NUM_WORKER_THREADS)]

def get_queue_index(paste_id):
    """Distribute pastes across queues based on hash of ID"""
    if paste_id:
        return hash(paste_id) % NUM_WORKER_THREADS
    return 0  # Default queue for new pastes without ID

def batch_worker(worker_id):
    """Background worker thread that processes a specific paste queue."""
    while True:
        current_time = time.time()
        should_process = False
        
        with batch_locks[worker_id]:
            queue_size = paste_queues[worker_id].qsize()
            time_elapsed = current_time - last_batch_executions[worker_id]
            
            if queue_size >= MAX_BATCH_SIZE or (queue_size > 0 and time_elapsed >= BATCH_INTERVAL):
                should_process = True
                
        if should_process:
            process_batch(worker_id)
            with batch_locks[worker_id]:
                last_batch_executions[worker_id] = time.time()
        
        # Adaptive sleep based on queue size
        sleep_time = 0.1 if paste_queues[worker_id].qsize() > 0 else 0.5
        time.sleep(sleep_time)

def process_batch(worker_id):
    """Process accumulated paste records in batch for a specific worker."""
    from shared.database import get_db
    
    batch_items = []
    batch_redis_updates = []
    
    try:
        db = next(get_db())
        
        queue_size = min(paste_queues[worker_id].qsize(), MAX_BATCH_SIZE)
        for _ in range(queue_size):
            if not paste_queues[worker_id].empty():
                try:
                    item = paste_queues[worker_id].get_nowait()
                    batch_items.append(item["paste_obj"])
                    batch_redis_updates.append(item)
                except queue.Empty:
                    break
        
        if not batch_items:
            return
            
        db.add_all(batch_items)
        db.commit()
        
        # Use Redis pipeline for bulk updates
        redis_conn = batch_redis_updates[0]["redis"] if batch_redis_updates else None
        if redis_conn:
            with redis_conn.pipeline() as pipe:
                for i, paste_obj in enumerate(batch_items):
                    db.refresh(paste_obj)
                    item = batch_redis_updates[i]
                    
                    paste_schema = paste.Paste.from_orm(paste_obj)
                    paste_key = f"paste:{paste_obj.id}"
                    pipe.set(paste_key, paste_schema.json())
                    pipe.expire(paste_key, 3600)  # Increase cache TTL to 1 hour
                    
                    if "callback" in item and item["callback"]:
                        item["callback"](paste_schema)
                
                pipe.execute()
            
        logger.info(f"Worker {worker_id}: Successfully processed batch of {len(batch_items)} pastes")
            
    except Exception as e:
        logger.error(f"Worker {worker_id}: Error processing batch: {str(e)}")
        try:
            db.rollback()
        except:
            pass
        
        for item in batch_redis_updates:
            queue_index = get_queue_index(item["paste_obj"].id)
            paste_queues[queue_index].put(item)
    finally:
        db.close()

# Start multiple worker threads
for i in range(NUM_WORKER_THREADS):
    worker_thread = threading.Thread(target=batch_worker, args=(i,), daemon=True)
    worker_thread.start()

def create_paste(db: Session, paste_data: paste.PasteCreate, redis, current_user = None, sync=False):
    """
    Create a new paste record with improved batching.
    """
    db_paste = Paste(
        **paste_data.dict(),
        user_id=current_user.id if current_user else None
    )
    
    if sync:
        db.add(db_paste)
        db.commit()
        db.refresh(db_paste)
        paste_schema = paste.Paste.from_orm(db_paste)
        
        paste_key = f"paste:{db_paste.id}"
        with redis.pipeline() as pipe:
            pipe.set(paste_key, paste_schema.json())
            pipe.expire(paste_key, 3600)  # 1 hour cache
            pipe.execute()
            
        return paste_schema
    else:
        result_queue = queue.Queue(1)
        
        def set_result(result):
            result_queue.put(result)
        
        queue_item = {
            "paste_obj": db_paste,
            "redis": redis,
            "callback": set_result
        }
        
        # Add to appropriate queue based on ID hash (or queue 0 for new pastes)
        paste_queues[0].put(queue_item)
        
        try:
            # Shorter timeout to prevent user waiting
            return result_queue.get(timeout=5)
        except queue.Empty:
            logger.warning("Batch processing timeout, falling back to sync processing")
            return create_paste(db, paste_data, redis, current_user, sync=True)


def get_paste(db: Session, paste_id: str, redis):
    paste_key = f"paste:{paste_id}"
    increment_key = f"paste:{paste_id}:views_increment"
    
    # OPTIMIZATION: Pipeline Redis operations and increase cache TTL
    with redis.pipeline() as pipe:
        pipe.get(paste_key)
        pipe.get(increment_key)
        results = pipe.execute()
    
    cached_paste, increment = results[0], int(results[1] or 0)
    
    if cached_paste:
        paste_schema = paste.Paste.parse_raw(cached_paste)
        # Increase TTL for frequently accessed pastes
        redis.expire(paste_key, 3600)  # Increase to 1 hour
    else:
        db_paste = db.query(Paste).filter(Paste.id == paste_id).first()
        if not db_paste or not db_paste.is_active:
            return None
        paste_schema = paste.Paste.from_orm(db_paste)
        
        # Use pipeline for setting cache
        with redis.pipeline() as pipe:
            pipe.set(paste_key, paste_schema.json())
            pipe.expire(paste_key, 3600)  # Increase to 1 hour
            pipe.execute()

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