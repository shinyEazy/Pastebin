from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from shared.schemas import paste
from shared.database import get_db
from shared.schemas import paste as paste_schema
from shared.models.paste import Paste
from shared.redis import get_redis
from app import getUser
from typing import List, Optional

router = APIRouter()

@router.post("/pastes/", response_model=paste.Paste)
def create_paste(paste: paste.PasteCreate, db: Session = Depends(get_db), redis=Depends(get_redis), user_id: Optional[int] = Depends(getUser.get_current_user)):
    return crud.create_paste(db, paste, redis, user_id=user_id)

@router.get("/pastes/{paste_id}", response_model=paste.Paste)
def read_paste(paste_id: str, db: Session = Depends(get_db), redis=Depends(get_redis)):
    paste = crud.get_paste(db, paste_id, redis)
    if paste is None:
        raise HTTPException(status_code=404, detail="Paste not found or expired")
    return paste

@router.get("/user-pastes", response_model=List[str])  
def get_user_pastes(
    db: Session = Depends(get_db),
    user_id: Optional[int] = Depends(getUser.get_current_user)
):
    if not user_id:
        return []  
    return crud.get_pastes_by_user_id(db, user_id)


