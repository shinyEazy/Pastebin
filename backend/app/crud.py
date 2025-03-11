from sqlalchemy.orm import Session
from app.models.paste import Paste
from datetime import datetime

def create_paste(db: Session, paste_data):
    db_paste = Paste(**paste_data.dict())
    db.add(db_paste)
    db.commit()
    db.refresh(db_paste)
    return db_paste

def get_paste(db: Session, paste_id: int):
    paste = db.query(Paste).filter(Paste.id == paste_id).first()
    if paste and paste.expire_at and paste.expire_at < datetime.utcnow():
        db.delete(paste)
        db.commit()
        return None
    
    if paste:
        paste.views += 1
        db.commit()
        db.refresh(paste)

    return paste