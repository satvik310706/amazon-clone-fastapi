from fastapi import APIRouter, Depends, HTTPException
from products.services import *
from dependencies.auth_dep import get_current_user
from products.schemas import *
product_router=APIRouter()
@product_router.get('/', response_model=list[ProductResponse])
async def get_product():
    products = await get_all_products()
    if products:
        return products
    else:
        raise HTTPException(status_code=404, detail="No products found")
@product_router.get('/{product_id}',response_model=ProductResponse)
async def get_product_by_id(product_id: int):
    product = await get_product_by_id(product_id)
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")
@product_router.post('/',response_model=ProductResponse)
async def create_a_product(product:ProductCreate, current_user=Depends(get_current_user)):
    answer = await create_product(product, current_user["id"])
    if not answer:
        raise HTTPException(status_code=400, detail="Product creation failed")
    return answer 
@product_router.put('/{product_id}',response_model=ProductResponse)
async def update_a_product(product_id:str, product:ProductUpdate, current_user=Depends(get_current_user)):
    answer = await update_product(product_id, product, current_user)
    if not answer:
        raise HTTPException(status_code=400, detail="Product update failed")
    return answer
@product_router.delete('/{product_id}')
async def remove_product(product_id: str, user=Depends(get_current_user)):
    return await delete_product(product_id, user)