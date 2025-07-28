from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL
client = AsyncIOMotorClient(MONGO_URL)
db=client["amazon_app"]
user_collection = db["users"]
product_collection = db["products"]
order_collection = db["orders"]
cart_collection = db.get_collection("cart")
order_collection = db["orders"]
