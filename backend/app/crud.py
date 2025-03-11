from sqlalchemy.orm import Session
from app.models.paste import Paste
from app.utils import is_expired
import logging

logging.basicConfig(
    filename="app.log",  
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

def create_paste(db: Session, paste_data):
    db_paste = Paste(**paste_data.dict())
    db.add(db_paste)
    db.commit()
    db.refresh(db_paste)
    return db_paste

def get_paste(db: Session, paste_id: int):
    paste = db.query(Paste).filter(Paste.id == paste_id).first()

    if not paste:
        logging.info(f"Paste {paste_id} not found.")
        return None  

    if not paste.is_active:
        logging.info(f"Paste {paste_id} is inactive.")
        return None  

    logging.info(f"Checking paste {paste_id} - Expiration: {paste.expiration}, Created At: {paste.created_at}, Views: {paste.views}")

    if is_expired(paste):
        logging.info(f"Paste {paste_id} has expired. Marking as inactive.")
        paste.is_active = False
        db.commit()
        return None

    paste.views += 1
    db.commit()
    db.refresh(paste)

    logging.info(f"Paste {paste_id} accessed. New view count: {paste.views}")

    return paste
