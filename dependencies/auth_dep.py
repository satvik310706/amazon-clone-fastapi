from bson.objectid import ObjectId
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from auth.jwt import decode_access_token
from database import user_collection

bearer_scheme = HTTPBearer()

def serialize_user(user):
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "role": user["role"]
    }

async def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization token missing")

    try:
        payload = decode_access_token(token.split(" ")[1])
        user = await user_collection.find_one({"_id": ObjectId(payload.get("id"))})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return serialize_user(user)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
async def get_current_admin(request: Request):
    user = await get_current_user(request)
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="You are not an admin")
    return user

async def get_current_dealer(request: Request):
    user = await get_current_user(request)
    if user["role"] != "dealer":
        raise HTTPException(status_code=403, detail="You are not a dealer")
    return user
from fastapi import Depends

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, user=Depends(get_current_user)):
        if user["role"] not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="You don't have permission")
