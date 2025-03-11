from sqlalchemy.orm import Session
from app.models.paste import Paste

def create_paste(db: Session, paste_data):
    db_paste = Paste(**paste_data.dict())
    db.add(db_paste)
    db.commit()
    db.refresh(db_paste)
    return db_paste

def get_paste(db: Session, paste_id: int):
    return db.query(Paste).filter(Paste.id == paste_id).first()