from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class CartItemModel(BaseModel):
    product_id: str
    quantity: int

class CartDBModel(CartItemModel):
    user_id: str