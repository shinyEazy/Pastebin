from shared.database import get_db
from shared.models.paste import Paste
from shared.utils import is_expired

def cleanup_expired_pastes():
    db = next(get_db())
    try:
        pastes = db.query(Paste).filter(Paste.is_active == True).all()
        for paste in pastes:
            if is_expired(paste):
                paste.is_active = False
        db.commit()
    finally:
        db.close()
