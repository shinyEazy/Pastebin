from jose import JWTError, jwt
from fastapi import Request

SECRET_KEY = "secret"
ALGORITHM = "HS256"

def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        print("⚠️ No Authorization header found.")
        return None

    token = auth_header.split("Bearer ")[1]
    print("📩 Received token:", token)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("📤 Payload decode:", payload)
        user_id: int = payload.get("id")
        print("👤 User ID:", user_id)
        return user_id
    except JWTError as e:
        print("❌ Token decode failed:", e)
        return None
