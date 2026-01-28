from pymongo import MongoClient
from datetime import datetime
import config

client = MongoClient(config.MONGO_URL)
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
# Expire a session
# -----------------------
def expire_session(session_id):
    sessions_col.update_one(
        {"session_id": session_id},
        {"$set": {"revoked": True, "revoked_at": datetime.utcnow()}}
    )

# -----------------------
# Add / Remove country
# -----------------------
def add_country(country_name):
    """
    Add a country if it doesn't exist.
    Creates a dummy session for the country to hold stock/prices.
    """
    exists = sessions_col.find_one({"country": country_name})
    if not exists:
        sessions_col.insert_one({
            "session_id": f"country_{country_name}_{datetime.utcnow().timestamp()}",
            "country": country_name,
            "price": 0,
            "stock": 0,
            "string": None,
            "two_step": False,
            "added_by": None,
            "created_at": datetime.utcnow(),
            "revoked": False
        })

def remove_country(country_name):
    """
    Remove all sessions for a given country.
    """
    sessions_col.delete_many({"country": country_name})

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
# Set / Get price
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
    return list(sessions_col.distinct("country"))

# -----------------------
# Get country info by name
# -----------------------
def get_country_info(country):
    return sessions_col.find_one({"country": country})

# -----------------------
# Assign session to user (dummy, can be extended)
# -----------------------
def assign_session_to_user(user_id, session_id):
    sessions_col.update_one(
        {"session_id": session_id},
        {"$set": {"assigned_to": user_id, "assigned_at": datetime.utcnow()}}
    )