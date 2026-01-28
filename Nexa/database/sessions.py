# Nexa/database/sessions.py
from pymongo import MongoClient
from datetime import datetime
import config

client = MongoClient(config.MONGO_URI)
db = client['nexa_bot']

sessions_col = db.sessions

# -----------------------
# Add a session
# -----------------------
def add_session(country, price, stock, string, two_step=False, added_by=None):
    session = {
        "session_id": string[:10] + str(datetime.utcnow().timestamp()),
        "country": country,
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
        {"$set": {"revoked": True, "revoked_by": revoked_by, "revoked_at": revoked_at}}
    )

# -----------------------
# List all sessions
# -----------------------
def list_sessions():
    return list(sessions_col.find())

# -----------------------
# Get single session by ID
# -----------------------
def get_session(session_id):
    return sessions_col.find_one({"session_id": session_id})

# -----------------------
# Get all available countries
# -----------------------
def get_available_countries():
    return sessions_col.distinct("country")

# -----------------------
# Update stock for country
# -----------------------
def update_stock(country, qty):
    sessions_col.update_many({"country": country}, {"$inc": {"stock": qty}})

# -----------------------
# Set/Get price
# -----------------------
def set_price(country, price):
    sessions_col.update_many({"country": country}, {"$set": {"price": price}})

def get_price(country):
    s = sessions_col.find_one({"country": country})
    return s.get("price") if s else None

# -----------------------
# Get all countries
# -----------------------
def get_countries():
    return list(sessions_col.find().distinct("country"))