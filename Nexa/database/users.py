from Nexa.database.mongo import users
from datetime import datetime
import config


def create_user(user_id: int, username: str | None):
    users.update_one(
        {"user_id": user_id},
        {
            "$setOnInsert": {
                "user_id": user_id,
                "username": username,
                "balance": 0,
                "created_at": datetime.utcnow()
            }
        },
        upsert=True
    )


def update_username(user_id: int, username: str):
    users.update_one(
        {"user_id": user_id},
        {"$set": {"username": username}}
    )


def get_user(user_id: int):
    return users.find_one({"user_id": user_id})


def get_balance(user_id: int) -> int:
    user = users.find_one({"user_id": user_id})
    return user.get("balance", 0) if user else 0


def deduct_balance(user_id: int, amount: float) -> bool:
    res = users.update_one(
        {"user_id": user_id, "balance": {"$gte": amount}},
        {"$inc": {"balance": -amount}}
    )
    return res.modified_count == 1


def add_balance(user_id: int, amount: float):
    users.update_one(
        {"user_id": user_id},
        {"$inc": {"balance": amount}}
    )


def is_admin(user_id: int) -> bool:
    return user_id in config.ADMINS

# -----------------------
# Ensure user exists in DB
# -----------------------
def ensure_user(user_id, username=None):
    """
    Creates the user if it doesn't exist.
    Updates username if provided.
    Returns the user document.
    """
    user = get_user(user_id)
    if user is None:
        create_user(user_id, username=username)
        user = get_user(user_id)
    elif username and user.get("username") != username:
        update_username(user_id, username)
        user = get_user(user_id)
    return user