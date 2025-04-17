from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from shared.schemas import paste
from shared.database import get_db
from shared.redis import get_redis
from app.dependencies import get_current_user
from shared.models.user import User

router = APIRouter()

@router.post("/pastes", response_model=paste.Paste)
def create_paste(
    paste: paste.PasteCreate,
    db: Session = Depends(get_db),
    redis=Depends(get_redis),
    current_user: User = Depends(get_current_user)
):
    return crud.create_paste(db, paste, redis, current_user)

@router.get("/pastes/{paste_id}", response_model=paste.Paste)
def read_paste(paste_id: str, db: Session = Depends(get_db), redis=Depends(get_redis)):
    paste = crud.get_paste(db, paste_id, redis)
    if paste is None:
        raise HTTPException(status_code=404, detail="Paste not found or expired")
    return paste