from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.users import users_db

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
token_auth_scheme = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if hashed_password is None:
        return False
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

def create_access_token(data: dict, expires_minutes: Optional[int] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=(expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(token_auth_scheme)
) -> Dict[str, Any]:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")
        user_id = payload.get("user_id")

        if email is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user = users_db.get(email)
        if not user or user.get("status") != "active":
            raise HTTPException(status_code=403, detail="User not active or not found")

        return {"email": email, "role": role, "user_id": user_id}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
