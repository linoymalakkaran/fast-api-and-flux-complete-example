from fastapi import APIRouter, Depends
from app.core.auth import get_current_active_user

router = APIRouter()

@router.get("/users/me", tags=["user"])
async def read_users_me(current_user = Depends(get_current_active_user)):
    return current_user
