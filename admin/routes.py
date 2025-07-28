from fastapi import APIRouter, Depends
from dependencies.auth_dep import get_current_user, RoleChecker
from admin.services import (
    get_all_users, delete_user_or_dealer, get_admin_stats
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

admin_only = RoleChecker(["admin"])

@router.get("/users")
async def fetch_users(_: None = Depends(admin_only)):
    return await get_all_users()

@router.delete("/delete/{user_id}")
async def delete_user(user_id: str, _: None = Depends(admin_only)):
    return await delete_user_or_dealer(user_id)

@router.get("/stats")
async def admin_stats(_: None = Depends(admin_only)):
    return await get_admin_stats()
