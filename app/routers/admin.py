from fastapi import APIRouter, Depends
from app.core.auth import get_admin_user

router = APIRouter()

@router.get("/admin", tags=["admin"])
async def read_admin(current_user = Depends(get_admin_user)):
    return {"msg": "Welcome, admin!"}
