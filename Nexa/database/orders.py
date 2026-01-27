from Nexa.database.mongo import db
from datetime import datetime
import uuid

orders = db.orders


def create_order(user_id, session, status="active"):
    order_id = str(uuid.uuid4())
    orders.insert_one({
        "order_id": order_id,
        "user_id": user_id,
        "session_id": session["_id"],
        "country": session["country"],
        "price": session["price"],
        "status": status,
        "created_at": datetime.utcnow(),
        "expires_at": session.get("expires_at")
    })
    return order_id


def update_order_status(session_id, status: str):
    orders.update_one(
        {"session_id": session_id},
        {"$set": {"status": status}}
    )


def get_user_orders(user_id: int):
    """Get all orders of a user sorted by newest first"""
    return list(
        orders.find({"user_id": user_id}).sort("created_at", -1)
    )


def get_order(order_id: str):
    """Get a single order by order_id"""
    return orders.find_one({"order_id": order_id})


def get_total_orders(user_id: int = None) -> int:
    """Return total number of orders in database"""
    if user_id:
        return orders.count_documents({"user_id": user_id})
    return orders.count_documents({})