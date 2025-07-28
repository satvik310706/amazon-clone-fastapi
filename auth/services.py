from auth.schemas import *
from auth.utils import hash_password, verify_password
from auth.models import serialize_user
from auth.jwt import create_access_token
from database import user_collection
from bson.objectid import ObjectId
async def register_user(user:UserRegister)-> UserResponse:
    existing_user = await user_collection.find_one({"email":user.email})
    if not existing_user:
        user_data = user.dict()
        user_data['password']=hash_password(user_data['password'])
        result = await user_collection.insert_one(user_data)
        user_data['_id'] = str(result.inserted_id)
        return serialize_user(user_data)
async def login_user(user:UserLogin)->TokenData:
    existing_user = await user_collection.find_one({"email":user.email})
    if existing_user and verify_password(user.password, existing_user['password']):
        access_token = create_access_token({"email": existing_user['email'], "id": str(existing_user['_id']), "role": existing_user.get('role')})
        return {"access_token": access_token, "token_type": "bearer"}
async def update_user(data:UserUpdate, user_id:str):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    if 'password' in update_data:
        update_data['password'] = hash_password(update_data['password'])
    result = await user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    updated_user = await user_collection.find_one({"_id": ObjectId(user_id)})
    return serialize_user(updated_user)