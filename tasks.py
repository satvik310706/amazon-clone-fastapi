from celery import Celery

# Initialize Celery app
celery = Celery(__name__, broker='redis://localhost:6379/0')

@celery.task
def cart_reminder_task(user_email: str, username: str, cart_items: list):
    item_names = ', '.join(cart_items)
    print(f"📩 Hey {username}, the items [{item_names}] are still waiting in your cart!")
