from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "secret"  
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
  # không dùng nhưng vẫn cần

def get_current_user(token: str = Depends(oauth2_scheme)):
    print("📩 Received token:", token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("📤 Payload decode:", payload)
        user_id: int = payload.get("id")
        print("👤 User ID:", user_id)
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception
