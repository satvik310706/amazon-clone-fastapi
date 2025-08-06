from database import user_collection, order_collection, product_collection
from bson import ObjectId
from fastapi import HTTPException
from products.models import serialize_product
async def get_all_users():
    users = await user_collection.find({}, {"password": 0}).to_list(100)
    for user in users:
        user["_id"] = str(user["_id"])
    return users
async def get_all_products():
    products = await product_collection.find().to_list(None)
    list_of_products=[]
    for i in products:
        list_of_products.append(serialize_product(i))
    return list_of_products
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
async def update_dealer_product(product_id: str, updated_data: dict, dealer_id: str):
    product = await product_collection.find_one({"_id": ObjectId(product_id)})
    if not product or product["created_by"] != dealer_id:
        raise HTTPException(status_code=403, detail="Not your product")
    await product_collection.update_one({"_id": ObjectId(product_id)}, {"$set": updated_data})
    return {"message": "Product updated"}

# ✅ Delete a dealer product
async def delete_dealer_product(product_id: str, dealer_id: str):
    product = await product_collection.find_one({"_id": ObjectId(product_id)})
    if not product or product["created_by"] != dealer_id:
        raise HTTPException(status_code=403, detail="Not your product")
    await product_collection.delete_one({"_id": ObjectId(product_id)})
    return {"message": "Product deleted"}
