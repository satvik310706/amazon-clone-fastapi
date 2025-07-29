from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from dependencies.auth_dep import get_current_user
from orders.services import place_order, get_user_orders, get_all_orders, update_order_status
from database import order_collection
from bson import ObjectId, errors
from orders.utils import *
router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/place")
async def place_order_route(user=Depends(get_current_user)):
    return await place_order(user["id"])

@router.get("/my-orders")
async def get_my_orders(user=Depends(get_current_user)):
    orders = await order_collection.find({"user_id": user["id"]}).to_list(None)

    # ✅ Convert ObjectId to string
    for order in orders:
        order["_id"] = str(order["_id"])
        order["user_id"] = str(order["user_id"])
        for item in order.get("items", []):
            item["product_id"] = str(item["product_id"])

    return orders

@router.get("/all")
async def get_all_orders(user=Depends(get_current_user)):
    # Ensure only admin sees all orders (optional check)
    if user["role"] != "admin":
        return {"error": "Unauthorized"}

    orders = await order_collection.find().to_list(None)

    # ✅ Convert ObjectIds
    return [serialize_order(order) for order in orders]
# orders/routes.py

class StatusUpdate(BaseModel):
    status: str

@router.put("/{order_id}/status")
async def update_order_status(order_id: str, data: StatusUpdate, user=Depends(get_current_user)):
    # Step 1: Validate ObjectId
    try:
        obj_id = ObjectId(order_id)
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Order ID format")

    # Step 2: Run update
    result = await order_collection.update_one(
        {"_id": obj_id},
        {"$set": {"status": data.status}}
    )

    # Step 3: Handle no match
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": f"Order {order_id} status updated to {data.status}"}