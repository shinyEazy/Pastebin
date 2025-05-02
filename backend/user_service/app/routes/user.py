from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from shared.database import get_db
from shared.models.paste import Paste
from shared.schemas.paste import Paste as PasteSchema
from shared.models.user import User
from ..dependencies import get_current_user

router = APIRouter()

@router.get("/pastes", response_model=list[PasteSchema])
def get_user_pastes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    print(f"Fetching pastes for user: {current_user.username}")
    pastes = db.query(Paste).filter(Paste.user_id == current_user.id, Paste.is_active == True).all()
    print(f"Found {len(pastes)} pastes")
    return pastes
