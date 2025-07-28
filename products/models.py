def serialize_product(product)->dict:
    return {
        "id": str(product["_id"]),
        "title": product["title"],
        "description": product["description"],
        "price": product["price"],
        "quantity": product["quantity"],
        "category": product["category"],
        "image_url": product["image_url"],
        "created_by": product["created_by"]
    }