# Nexa/database/sessions.py
from pymongo import MongoClient
from datetime import datetime, timedelta
import config

client = MongoClient(config.MONGO_URL)
db = client['nexa_bot']

sessions_col = db.sessions
countries_col = db.countries  # optional if you want a separate countries collection


# -----------------------
# Normalize country name
# -----------------------
def normalize_country(name: str) -> str:
    return name.strip().title()


# -----------------------
# Add a session
# -----------------------
def add_session(country, price, stock, string, two_step=False, added_by=None):
    session = {
        "session_id": string[:10] + str(datetime.utcnow().timestamp()),
        "country": normalize_country(country),
        "price": price,
        "stock": stock,
        "string": string,
        "two_step": two_step,
        "added_by": added_by,
        "created_at": datetime.utcnow(),
        "revoked": False
    }
    sessions_col.insert_one(session)
    return session


# -----------------------
# Remove a session
# -----------------------
def remove_session(session_id):
    sessions_col.delete_one({"session_id": session_id})


# -----------------------
# Revoke a session
# -----------------------
def revoke_session(session_id, revoked_by=None, revoked_at=None):
    sessions_col.update_one(
        {"session_id": session_id},
        {"$set": {"revoked": True, "revoked_by": revoked_by, "revoked_at": revoked_at or datetime.utcnow()}}
    )


# -----------------------
# List all sessions
# -----------------------
def list_sessions():
    return list(sessions_col.find())


# -----------------------
# Get a single session
# -----------------------
def get_session(session_id):
    return sessions_col.find_one({"session_id": session_id})


# -----------------------
# Get active (non-revoked) sessions
# -----------------------
def get_active_sessions():
    return list(sessions_col.find({"revoked": False}))


# -----------------------
# Assign session to user (mark as used)
# -----------------------
def assign_session_to_user(session_id, user_id):
    sessions_col.update_one(
        {"session_id": session_id},
        {"$set": {"assigned_to": user_id, "assigned_at": datetime.utcnow()}}
    )


# -----------------------
# Expire session (custom logic)
# -----------------------
def expire_session(session_id):
    sessions_col.update_one(
        {"session_id": session_id},
        {"$set": {"revoked": True, "revoked_at": datetime.utcnow()}}
    )


# -----------------------
# Get all available countries
# -----------------------
def get_available_countries():
    return sessions_col.distinct("country")


# -----------------------
# Get country info by name
# -----------------------
def get_country_info(country):
    return sessions_col.find_one({"country": normalize_country(country)})


# -----------------------
# Update stock
# -----------------------
def update_stock(country, qty):
    sessions_col.update_many({"country": normalize_country(country)}, {"$inc": {"stock": qty}})


# -----------------------
# Set price
# -----------------------
def set_price(country, price):
    sessions_col.update_many({"country": normalize_country(country)}, {"$set": {"price": price}})


# -----------------------
# Get price
# -----------------------
def get_price(country):
    s = sessions_col.find_one({"country": normalize_country(country)})
    return s.get("price") if s else None


# -----------------------
# Get all countries
# -----------------------
def get_countries():
    return list(sessions_col.find().distinct("country"))


# -----------------------
# Add country
# -----------------------
def add_country(name):
    name = normalize_country(name)
    if not sessions_col.find_one({"country": name}):
        sessions_col.insert_one({"country": name, "price": 0, "stock": 0})


# -----------------------
# Remove country
# -----------------------
def remove_country(name):
    name = normalize_country(name)
    sessions_col.delete_many({"country": name})