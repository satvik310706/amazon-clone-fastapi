from database import user_collection, order_collection, product_collection
from bson import ObjectId
from fastapi import HTTPException

async def get_all_users():
    users = await user_collection.find({}, {"password": 0}).to_list(100)
    for user in users:
        user["_id"] = str(user["_id"])
    return users

async def delete_user_or_dealer(user_id: str):
    result = await user_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

async def get_admin_stats():
    user_count = await user_collection.count_documents({})
    product_count = await product_collection.count_documents({})
    order_count = await order_collection.count_documents({})
    return {
        "total_users": user_count,
        "total_products": product_count,
        "total_orders": order_count
    }
