from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from shared.schemas import paste
from shared.database import get_db
from shared.schemas import paste as paste_schema
from shared.models.paste import Paste
from shared.redis import get_redis
from app import getUser
from typing import List

router = APIRouter()

@router.post("/pastes/", response_model=paste.Paste)
def create_paste(paste: paste.PasteCreate, db: Session = Depends(get_db), redis=Depends(get_redis), user_id: int = Depends(getUser.get_current_user)):
    return crud.create_paste(db, paste, redis, user_id=user_id)

@router.get("/pastes/{paste_id}", response_model=paste.Paste)
def read_paste(paste_id: int, db: Session = Depends(get_db), redis=Depends(get_redis)):
    paste = crud.get_paste(db, paste_id, redis)
    if paste is None:
        raise HTTPException(status_code=404, detail="Paste not found or expired")
    return paste

@router.get("/pastes/me", response_model=List[paste_schema.Paste])
def get_my_pastes(
    db: Session = Depends(get_db),
    current_user: dict = Depends(getUser.get_current_user)  # {'id': user_id, ...}
):
    user_id = current_user["id"]
    pastes = db.query(Paste).filter(Paste.user_id == user_id).all()
    return pastes