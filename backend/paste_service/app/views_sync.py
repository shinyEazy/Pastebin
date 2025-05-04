import redis
from shared.config import settings
import logging
import time
from apscheduler.triggers.interval import IntervalTrigger
from shared.database import get_db
from shared.models.paste import Paste

logger = logging.getLogger(__name__)

# Create a Redis connection pool
redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    max_connections=100,  # Increase for high concurrency
    socket_timeout=10,
    socket_connect_timeout=10,
    health_check_interval=30,
    retry_on_timeout=True
)

def get_redis():
    """Get a Redis connection from the pool"""
    return redis.Redis(connection_pool=redis_pool)

def sync_paste_views(db, redis):
    """
    Optimized function to sync paste view counts from Redis to database
    """
    start_time = time.time()

    # Get all paste IDs that need syncing (using SSCAN instead of SMEMBERS for large sets)
    all_paste_ids = []
    cursor = 0
    while True:
        cursor, batch = redis.sscan("pastes_to_sync", cursor, count=1000)
        all_paste_ids.extend(batch)
        if cursor == 0:
            break
    
    if not all_paste_ids:
        return

    paste_ids = [pid.decode('utf-8') if isinstance(pid, bytes) else pid for pid in all_paste_ids]
    logger.info(f"Syncing view counts for {len(paste_ids)} pastes")

    # Process in batches of 1000
    batch_size = 1000
    
    for i in range(0, len(paste_ids), batch_size):
        batch = paste_ids[i:i+batch_size]
        updates = {}
        
        # Use Redis pipeline for batch operations
        with redis.pipeline() as pipe:
            for paste_id in batch:
                increment_key = f"paste:{paste_id}:views_increment"
                pipe.get(increment_key)
                pipe.srem("pastes_to_sync", paste_id)
                pipe.delete(increment_key)
            
            results = pipe.execute()
        
        # Process results in groups of 3 (get, srem, delete)
        for j in range(0, len(results), 3):
            if j + 2 < len(results):
                paste_id = batch[j // 3]
                increment = int(results[j] or 0)
                
                if increment > 0:
                    updates[paste_id] = increment
        
        # Optimize database update
        if updates:
            try:
                # Use bulk update with a single transaction
                for paste_id, increment in updates.items():
                    db.query(Paste).filter(Paste.id == paste_id).update(
                        {"views": Paste.views + increment}
                    )
                
                db.commit()
                logger.info(f"Successfully updated {len(updates)} paste view counts")
            except Exception as e:
                db.rollback()
                logger.error(f"Error updating paste view counts: {str(e)}")
                
                # Put the items back in the sync set
                with redis.pipeline() as pipe:
                    for paste_id, increment in updates.items():
                        pipe.sadd("pastes_to_sync", paste_id)
                        pipe.set(f"paste:{paste_id}:views_increment", increment)
                    pipe.execute()

    duration = time.time() - start_time
    logger.info(f"View count sync completed in {duration:.2f} seconds")

# Add this to the app's scheduled tasks
def setup_views_sync_job(scheduler):
    """
    Set up scheduled job to sync view counts regularly.
    """
    from shared.database import get_db
    from shared.redis import get_redis
    
    def sync_job():
        db = next(get_db())
        redis = get_redis()
        try:
            sync_paste_views(db, redis)
        finally:
            db.close()
    
    # Run every minute
    scheduler.add_job(
        sync_job,
        trigger=IntervalTrigger(minutes=1),
        max_instances=1
    )
    return scheduler