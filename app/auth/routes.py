from fastapi import APIRouter, HTTPException, Depends

from app.auth.models import LoginRequest, TokenResponse
from app.auth.users import users_db
from app.core.security import verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    user = users_db.get(req.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if user.get("status") != "active":
        raise HTTPException(status_code=403, detail="User inactive or suspended")

    if not verify_password(req.password, user.get("hashed_password")):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({
        "sub": user["email"],
        "user_id": user["user_id"],
        "role": user["role"]
    })

    return {"access_token": token, "token_type": "bearer", "role": user["role"]}

@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return {"user": current_user}
