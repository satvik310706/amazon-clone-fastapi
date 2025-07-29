from fastapi import APIRouter, Depends, HTTPException
from cart.models import CartItemModel
from database import cart_collection, product_collection
from dependencies.auth_dep import get_current_user
from bson import ObjectId
from tasks import cart_reminder_task

router = APIRouter()

@router.post("/add")
async def add_to_cart(item: CartItemModel, user=Depends(get_current_user)):
    existing = await cart_collection.find_one({"user_id": user["id"], "product_id": item.product_id})
    if existing:
        await cart_collection.update_one(
            {"_id": existing["_id"]},
            {"$inc": {"quantity": item.quantity}}
        )
    else:
        await cart_collection.insert_one({
            "user_id": user["id"],
            "product_id": item.product_id,
            "quantity": item.quantity
        })

        # Fetch product details to include in the reminder message
        product = await product_collection.find_one({"_id": ObjectId(item.product_id)})
        if product:
            # Schedule reminder after 10 minutes
            cart_reminder_task.apply_async(
                args=[user["email"], user["username"], [product["title"]]],
                countdown=600  # 10 minutes in seconds
            )

    return {"message": "Item added to cart"}

@router.get("/")
async def get_cart(user=Depends(get_current_user)):
    cart_items = await cart_collection.find({"user_id": user["id"]}).to_list(None)
    results = []
    total = 0
    for item in cart_items:
        product = await product_collection.find_one({"_id": ObjectId(item["product_id"])})
        if product:
            item_info = {
                "title": product["title"],
                "price": product["price"],
                "quantity": item["quantity"],
                "product_id": str(product["_id"]),
                "subtotal": product["price"] * item["quantity"]
            }
            total += item_info["subtotal"]
            results.append(item_info)
    return {"cart": results, "total_price": total}

@router.delete("/{product_id}")
async def remove_from_cart(product_id: str, user=Depends(get_current_user)):
    result = await cart_collection.delete_one({"user_id": user["id"], "product_id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item removed from cart"}


@router.put("/update")
async def update_quantity(item: CartItemModel, user=Depends(get_current_user)):
    result = await cart_collection.update_one(
        {"user_id": user["id"], "product_id": item.product_id},
        {"$set": {"quantity": item.quantity}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Quantity updated"}
