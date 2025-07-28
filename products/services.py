from database import product_collection
from bson.objectid import ObjectId
from products.schemas import ProductCreate, ProductUpdate
from products.models import serialize_product
async def get_all_products():
    products = await product_collection.find().to_list(None)
    list_of_products=[]
    for i in products:
        list_of_products.append(serialize_product(i))
    return list_of_products
async def create_product(data:ProductCreate, user_id:str):
    product_data = data.dict()
    product_data["image_url"] = str(product_data["image_url"])  # ✅ Convert HttpUrl to string
    product_data["created_by"] = user_id

    result = await product_collection.insert_one(product_data)
    product_data["_id"]=result.inserted_id
    return serialize_product(product_data)
async def get_product_by_id(product_id:str):
    product = await product_collection.find_one({"_id":ObjectId(product_id)})
    if product:
        return serialize_product(product)
async def update_product(product_id:str, data:ProductUpdate, current_user):
    product = await product_collection.find_one({"_id":ObjectId(product_id)})
    if current_user['role'] == 'admin' or product['created_by']== current_user['id']:
        update_data = {k: v for k, v in data.dict(exclude_unset=True).items()}
        await product_collection.update_one({"_id":ObjectId(product_id)},{"$set":update_data})
        updated_product = await product_collection.find_one({"_id":ObjectId(product_id)})
        return serialize_product(updated_product)
async def delete_product(product_id:str, current_user):
    product = await product_collection.find_one({"_id":ObjectId(product_id)})
    if current_user['role'] == 'admin' or product['created_by']== current_user['id']:
        await product_collection.delete_one({"_id":ObjectId(product_id)})
        return {"message":"Product deleted..!!!"}