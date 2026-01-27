from Nexa.database.mongo import sessions, countries
from datetime import datetime, timedelta
from pymongo import ReturnDocument
import uuid


# -------------------- ADMIN FUNCTIONS --------------------

def add_country(name: str):
    """Add a country"""
    countries.update_one(
        {"name": name.upper()},
        {"$setOnInsert": {"name": name.upper(), "created_at": datetime.utcnow()}},
        upsert=True
    )


def remove_country(name: str):
    """Remove a country"""
    countries.delete_one({"name": name.upper()})


def get_countries():
    """Return all countries"""
    return list(countries.find({}))


def add_session(country: str, price: float, stock: int, string_session: str, two_step: bool, added_by: int):
    """Add a new session/number"""
    sessions.insert_one({
        "_id": str(uuid.uuid4()),
        "country": country.upper(),
        "price": price,
        "stock": stock,
        "string_session": string_session,
        "two_step": two_step,
        "active": True,
        "revoked": False,
        "sold": False,
        "added_by": added_by,
        "created_at": datetime.utcnow(),
        "expires_at": None
    })


def remove_session(session_id: str):
    """Remove a session completely"""
    sessions.delete_one({"_id": session_id})


def update_stock(session_id: str, delta: int):
    """Increase or decrease stock"""
    sessions.update_one({"_id": session_id}, {"$inc": {"stock": delta}})


def set_price(country: str, price: float):
    """Update price for all sessions of a country"""
    sessions.update_many(
        {"country": country.upper()},
        {"$set": {"price": price}}
    )


def get_price(country: str):
    """Get price of a country (first active session)"""
    session = sessions.find_one(
        {"country": country.upper(), "active": True, "revoked": False}
    )
    return session["price"] if session else None


def revoke_session(session_id: str, admin_id: int | None = None):
    """Revoke a live session"""
    sessions.update_one(
        {"_id": session_id},
        {"$set": {
            "active": False,
            "revoked": True,
            "revoked_at": datetime.utcnow(),
            "revoked_by": admin_id
        }}
    )


def expire_session(session_id: str):
    """Expire a sold session"""
    sessions.update_one(
        {"_id": session_id},
        {"$set": {
            "active": False,
            "expired": True,
            "expired_at": datetime.utcnow()
        }}
    )


# -------------------- USER FUNCTIONS --------------------

def get_available_countries():
    """Return countries with at least one available session"""
    return list(sessions.aggregate([
        {"$match": {"active": True, "revoked": False, "stock": {"$gt": 0}}},
        {"$group": {
            "_id": "$country",
            "price": {"$first": "$price"},
            "stock": {"$sum": "$stock"}
        }},
        {"$project": {
            "country": "$_id",
            "price": 1,
            "stock": 1,
            "_id": 0
        }}
    ]))


def get_active_session_by_chat(user_id: int):
    """Get active session for a user"""
    return sessions.find_one({
        "user_id": user_id,
        "sold": True,
        "active": True,
        "revoked": False
    })


def get_country_info(country: str):
    """Get info for a country (first active session)"""
    return sessions.find_one(
        {"country": country.upper(), "active": True, "revoked": False},
        sort=[("created_at", 1)]
    )


def assign_session_to_user(user_id: int, country: str, duration_min: int = 30):
    """Assign a session to a user, decrease stock automatically, mark sold, set expiry"""
    expires_at = datetime.utcnow() + timedelta(minutes=duration_min)

    return sessions.find_one_and_update(
        {
            "country": country.upper(),
            "active": True,
            "revoked": False,
            "stock": {"$gt": 0},
            "sold": False
        },
        {
            "$inc": {"stock": -1},
            "$set": {
                "user_id": user_id,
                "sold": True,
                "expires_at": expires_at
            }
        },
        return_document=ReturnDocument.AFTER
    )


def get_session(session_id: str):
    """Get a single session by session_id"""
    return sessions.find_one({"_id": session_id}) or sessions.find_one({"session_id": session_id})