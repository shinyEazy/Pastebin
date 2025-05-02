from sqlalchemy.orm import Session
import logging
import time
from shared.models.paste import Paste
from apscheduler.triggers.interval import IntervalTrigger

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def sync_paste_views(db: Session, redis):
    """
    Synchronize paste view counts from Redis to the database in batch.
    This should be called periodically to update the database.
    """
    start_time = time.time()
    
    # Get all paste IDs that need syncing
    paste_ids = redis.smembers("pastes_to_sync")
    if not paste_ids:
        return
    
    logger.info(f"Syncing view counts for {len(paste_ids)} pastes")
    
    # Process in batches of 500 to avoid memory issues with very large sets
    batch_size = 500
    paste_ids_list = list(paste_ids)
    
    for i in range(0, len(paste_ids_list), batch_size):
        batch = paste_ids_list[i:i+batch_size]
        
        # Create a dictionary to hold updates
        updates = {}
        
        # Process each paste in the batch
        for paste_id in batch:
            paste_id = paste_id.decode('utf-8') if isinstance(paste_id, bytes) else paste_id
            increment_key = f"paste:{paste_id}:views_increment"
            
            # Get view increment and reset counter
            increment = int(redis.get(increment_key) or 0)
            if increment > 0:
                updates[paste_id] = increment
                redis.delete(increment_key)
                redis.srem("pastes_to_sync", paste_id)
        
        # Perform batch update if we have any updates
        if updates:
            try:
                # Use SQLAlchemy's bulk update capabilities
                # This is more efficient than individual updates
                for paste_id, increment in updates.items():
                    # Note: In a real production system, you might want to use 
                    # a more efficient approach like raw SQL or the SQLAlchemy ORM bulk update
                    db.query(Paste).filter(Paste.id == paste_id).update(
                        {"views": Paste.views + increment}
                    )
                
                db.commit()
                logger.info(f"Successfully updated {len(updates)} paste view counts")
            except Exception as e:
                db.rollback()
                logger.error(f"Error updating paste view counts: {str(e)}")
                
                # Put the items back in the sync set
                for paste_id, increment in updates.items():
                    redis.sadd("pastes_to_sync", paste_id)
                    redis.set(f"paste:{paste_id}:views_increment", increment)
    
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