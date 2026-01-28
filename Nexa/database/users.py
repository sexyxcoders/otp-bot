from Nexa.database.mongo import db

users_col = db.users


def ensure_user(user_id: int, username: str = None):
    user = users_col.find_one({"user_id": user_id})
    if not user:
        users_col.insert_one({
            "user_id": user_id,
            "username": username,
            "balance": 0,
            "created_at": None
        })


def get_user(user_id: int):
    return users_col.find_one({"user_id": user_id})


def get_balance(user_id: int) -> int:
    user = get_user(user_id)
    return user["balance"] if user else 0


def add_balance(user_id: int, amount: int):
    users_col.update_one(
        {"user_id": user_id},
        {"$inc": {"balance": amount}},
        upsert=True
    )


def deduct_balance(user_id: int, amount: int) -> bool:
    user = get_user(user_id)
    if not user or user["balance"] < amount:
        return False

    users_col.update_one(
        {"user_id": user_id},
        {"$inc": {"balance": -amount}}
    )
    return True


def is_admin(user_id: int) -> bool:
    import config
    return user_id in config.ADMINS