from Nexa.database.mongo import db
from datetime import datetime

sessions_col = db.sessions


# ---------- COUNTRY ----------
def add_country(country: str, price: int):
    if sessions_col.find_one({"country": country}):
        return
    sessions_col.insert_one({
        "country": country,
        "price": price,
        "stock": 0,
        "created_at": datetime.utcnow()
    })


def remove_country(country: str):
    sessions_col.delete_many({"country": country})


def get_countries():
    return sessions_col.distinct("country")


def get_country_info(country: str):
    return sessions_col.find_one({"country": country})


# ---------- PRICE ----------
def set_price(country: str, price: int):
    sessions_col.update_many(
        {"country": country},
        {"$set": {"price": price}}
    )


def get_price(country: str):
    data = sessions_col.find_one({"country": country})
    return data["price"] if data else None


# ---------- SESSION ----------
def add_session(country: str, session_string: str, phone: str):
    sessions_col.insert_one({
        "country": country,
        "session_string": session_string,
        "phone": phone,
        "used": False,
        "assigned_to": None,
        "created_at": datetime.utcnow()
    })


def get_available_session(country: str):
    return sessions_col.find_one({
        "country": country,
        "used": False
    })


def mark_session_used(session_id, user_id):
    sessions_col.update_one(
        {"_id": session_id},
        {"$set": {"used": True, "assigned_to": user_id}}
    )


def expire_session(session_id):
    sessions_col.delete_one({"_id": session_id})


def revoke_session(session_id):
    expire_session(session_id)


def update_stock(country: str):
    return sessions_col.count_documents({
        "country": country,
        "used": False
    })