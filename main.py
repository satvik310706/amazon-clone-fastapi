from fastapi import FastAPI
from auth.routes import auth_router
from dealers.routes import router as dealer_router
from admin.routes import router as admin_router



from products.routes import product_router
from cart.routes import router as cart_router
from orders.routes import router as order_router

app=FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(cart_router, prefix="/cart", tags=["cart"])
app.include_router(dealer_router)
app.include_router(admin_router)
app.include_router(order_router)

app.include_router(product_router, prefix="/products", tags=["Products"])
@app.get("/")
def read_root():
    return {"message": "Welcome to Amazon App Backend"}