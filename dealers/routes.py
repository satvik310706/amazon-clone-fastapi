from fastapi import APIRouter, Depends
from dependencies.auth_dep import get_current_user, RoleChecker
from dealers.services import (
    get_dealer_products, get_dealer_orders, get_dealer_stats,
    create_product, update_dealer_product, delete_dealer_product
)

router = APIRouter(
    prefix="/dealer",
    tags=["Dealer"]
)

dealer_only = RoleChecker(["dealer"])

@router.get("/products")
async def dealer_products(user=Depends(get_current_user), _: None = Depends(dealer_only)):
    return await get_dealer_products(user["id"])

@router.post("/products")
async def add_product(product: dict, user=Depends(get_current_user), _: None = Depends(dealer_only)):
    return await create_product(product, user["id"])

@router.put("/products/{product_id}")
async def edit_product(product_id: str, updated_data: dict, user=Depends(get_current_user), _: None = Depends(dealer_only)):
    return await update_dealer_product(product_id, updated_data, user["id"])

@router.delete("/products/{product_id}")
async def remove_product(product_id: str, user=Depends(get_current_user), _: None = Depends(dealer_only)):
    return await delete_dealer_product(product_id, user["id"])

@router.get("/orders")
async def dealer_orders(user=Depends(get_current_user), _: None = Depends(dealer_only)):
    return await get_dealer_orders(user["id"])

@router.get("/stats")
async def dealer_stats(user=Depends(get_current_user), _: None = Depends(dealer_only)):
    return await get_dealer_stats(user["id"])
