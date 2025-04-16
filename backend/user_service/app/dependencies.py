from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from shared.database import get_db
from shared.models.user import User
from shared.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://auth_service:8001/auth/login", auto_error=False)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print(f"Received token: {token}")
    if not token:
        print("No token provided")
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        print(f"Decoded user_id: {user_id}")
        if not user_id:
            print("No user_id in token")
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        print(f"No user found for ID: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    print(f"Authenticated user: {user.username}")
    return user