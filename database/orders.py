from database.mongo import orders
import time

# Create new order
def create_order(user_id, phone, session):
    return orders.insert_one({
        "user_id": user_id,
        "phone": phone,
        "session": session,
        "otp": None,
        "status": "waiting",
        "created_at": int(time.time())
    }).inserted_id

# Set OTP and mark done
def set_otp(order_id, otp):
    orders.update_one(
        {"_id": order_id},
        {"$set": {"otp": otp, "status": "done"}}
    )

# Expire an order
def expire_order(order_id):
    orders.update_one(
        {"_id": order_id},
        {"$set": {"status": "expired"}}
    )

# Get latest order for a user
def get_latest_order(user_id):
    return orders.find_one(
        {"user_id": user_id},
        sort=[("_id", -1)]
    )