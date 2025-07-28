from database import product_collection, order_collection
from bson import ObjectId
from fastapi import HTTPException

# ✅ Create a product
async def create_product(product: dict, dealer_id: str):
    product["created_by"] = dealer_id
    result = await product_collection.insert_one(product)
    return {"message": "Product created", "product_id": str(result.inserted_id)}

# ✅ Get all dealer products
async def get_dealer_products(dealer_id: str):
    products = await product_collection.find({"created_by": dealer_id}).to_list(100)
    for p in products:
        p["_id"] = str(p["_id"])
    return products

# ✅ Update a dealer product
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

# ✅ Get only dealer’s items in all orders
async def get_dealer_orders(dealer_id: str):
    matching_orders = []

    all_orders = await order_collection.find().to_list(100)
    for order in all_orders:
        filtered_items = []
        for item in order["items"]:
            product = await product_collection.find_one({"_id": ObjectId(item["product_id"])})
            if product and product.get("created_by") == dealer_id:
                filtered_items.append(item)

        if filtered_items:
            order["_id"] = str(order["_id"])
            order["items"] = filtered_items
            matching_orders.append(order)

    return matching_orders

# Optional: For dashboard metrics
async def get_dealer_stats(dealer_id: str):
    product_count = await product_collection.count_documents({"created_by": dealer_id})
    orders = await get_dealer_orders(dealer_id)
    order_count = len(orders)
    return {"products": product_count, "orders": order_count}
