# orders/utils.py
def serialize_order(order):
    order["_id"] = str(order["_id"])
    order["user_id"] = str(order["user_id"])
    for item in order.get("items", []):
        item["product_id"] = str(item["product_id"])
    return order
