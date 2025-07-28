from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class OrderItemModel(BaseModel):
    product_id: str
    quantity: int
    price: float
    title: str

class OrderModel(BaseModel):
    user_id: str
    items: List[OrderItemModel]
    total_amount: float
    status: str = "Pending"  # Pending, Confirmed, Shipped, Delivered
    order_date: datetime = Field(default_factory=datetime.utcnow)
