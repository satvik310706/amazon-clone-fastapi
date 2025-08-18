from fastapi import APIRouter, HTTPException, Depends
from auth.schemas import *
from auth.services import register_user, login_user, update_user
from dependencies.auth_dep import get_current_user
auth_router = APIRouter()
@auth_router.get('/me')
async def get_my_profile(user=Depends(get_current_user)):
    return {
        "id": str(user["id"]),
        "name": user.get("username"),
        "email": user.get("email"),
        "role": user.get("role"),
        "phone": user.get("phone"),
        "address": user.get("address")
    }
@auth_router.post('/register', response_model=UserResponse)
async def register(user: UserRegister):
    a = await register_user(user)
    if not a:
        raise HTTPException(status_code=400, detail="User already exists")
    return a
@auth_router.post('/login', response_model=TokenData)
async def login(user:UserLogin):
    a = await login_user(user)
    if not a :
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return a
@auth_router.put('/update', response_model=UserResponse)
async def update(data:UserUpdate, current_user=Depends(get_current_user)):
    return await update_user(data, str(current_user["id"])) 