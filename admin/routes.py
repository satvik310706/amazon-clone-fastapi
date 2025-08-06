from fastapi import APIRouter, Depends
from dependencies.auth_dep import get_current_user, RoleChecker
from admin.services import *

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

admin_only = RoleChecker(["admin"])

@router.get("/users")
async def fetch_users(_: None = Depends(admin_only)):
    return await get_all_users()

@router.get("/products")
async def fetch_products(_: None = Depends(admin_only)):  # ✅ FIXED function name
    return await get_all_products()

@router.delete("/delete/{user_id}")
async def delete_user(user_id: str, _: None = Depends(admin_only)):
    return await delete_user_or_dealer(str(user_id))

@router.get("/stats")
async def admin_stats(_: None = Depends(admin_only)):
    return await get_admin_stats()

@router.put("/products/{product_id}")
async def edit_product(product_id: str, updated_data: dict, user=Depends(get_current_user), _: None = Depends(admin_only)):
    return await update_dealer_product(product_id, updated_data, user["id"])

@router.delete("/products/{product_id}")
async def remove_product(product_id: str, user=Depends(get_current_user), _: None = Depends(admin_only)):
    return await delete_dealer_product(product_id, user["id"])

