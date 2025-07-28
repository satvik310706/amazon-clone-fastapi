from database import cart_collection, order_collection, product_collection
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException

async def place_order(user_id: str):
    cart_items = await cart_collection.find({"user_id": user_id}).to_list(None)

    if not cart_items:
        return {"message": "Cart is empty"}

    order_items = []
    total_price = 0

    for item in cart_items:
        # ✅ Fetch the product info using product_id
        product = await product_collection.find_one({"_id": ObjectId(item["product_id"])})

        if not product:
            continue  # skip if product not found

        item_total = product["price"] * item["quantity"]
        total_price += item_total

        order_items.append({
            "product_id": str(item["product_id"]),
            "title": product["title"],
            "price": product["price"],
            "quantity": item["quantity"],
            "item_total": item_total,
            "dealer_id": product.get("created_by")  # ✅ Add dealer_id from product
        })

    order = {
        "user_id": user_id,
        "items": order_items,
        "total_price": total_price,
        "created_at": datetime.utcnow()
    }

    result = await order_collection.insert_one(order)
    await cart_collection.delete_many({"user_id": user_id})  # clear cart

    return {"order_id": str(result.inserted_id), "message": "Order placed successfully"}


async def get_user_orders(user_id: str):
    orders = await order_collection.find({"user_id": user_id}).to_list(length=None)
    return orders


async def get_all_orders():
    return await order_collection.find().to_list(length=None)


async def update_order_status(order_id: str, status: str):
    result = await order_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": status}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Order not found or status unchanged.")
    return {"message": "Order status updated"}
