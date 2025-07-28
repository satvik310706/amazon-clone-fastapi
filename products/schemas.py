from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
class ProductBase(BaseModel):
    title:str = Field(...,min_length=2, max_length=100)
    description: str = Field(..., min_length=2, max_length=500)
    price:float=Field(...,ge=0)
    quantity: int = Field(..., ge=0)
    category: str = Field(...)
    image_url: HttpUrl = Field(..., description="URL of the product image")
class ProductResponse(ProductBase):
    id:str
    created_by:str
class ProductCreate(ProductBase):
    pass 
class ProductUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    quantity: Optional[int]
    category: Optional[str]
