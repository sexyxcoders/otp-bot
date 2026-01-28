from pymongo import MongoClient
from datetime import datetime
import config

# -----------------------
# MongoDB setup
# -----------------------
client = MongoClient(config.MONGO_URL)
db = client['nexa_bot']

sessions_col = db.sessions
countries_col = db.countries  # optional if you track countries separately

# -----------------------
# Normalize country names
# -----------------------
def normalize_country(country: str):
    return country.strip().title()

# -----------------------
# Add a session
# -----------------------
def add_session(country, price, stock, string, two_step=False, added_by=None):
    session = {
        "session_id": string[:10] + str(int(datetime.utcnow().timestamp())),
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
        {"$set": {"revoked": True, "revoked_by": revoked_by, "revoked_at": revoked_at}}
    )

# -----------------------
# Expire a session (if needed)
# -----------------------
def expire_session(session_id):
    sessions_col.update_one(
        {"session_id": session_id},
        {"$set": {"revoked": True, "revoked_at": datetime.utcnow()}}
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
# Get active sessions (not revoked)
# -----------------------
def get_active_sessions():
    return list(sessions_col.find({"revoked": False}))

# -----------------------
# Assign a session to a user (mark as used)
# -----------------------
def assign_session_to_user(session_id, user_id):
    sessions_col.update_one(
        {"session_id": session_id},
        {"$set": {"assigned_to": user_id, "assigned_at": datetime.utcnow()}}
    )

# -----------------------
# Get all available countries
# -----------------------
def get_available_countries():
    return sessions_col.distinct("country")

# -----------------------
# Add country manually
# -----------------------
def add_country(country):
    country = normalize_country(country)
    if not sessions_col.find_one({"country": country}):
        sessions_col.insert_one({
            "country": country,
            "price": 0,
            "stock": 0,
            "created_at": datetime.utcnow()
        })

# -----------------------
# Remove country manually
# -----------------------
def remove_country(country):
    country = normalize_country(country)
    sessions_col.delete_many({"country": country})

# -----------------------
# Update stock for country
# -----------------------
def update_stock(country, qty):
    country = normalize_country(country)
    sessions_col.update_many({"country": country}, {"$inc": {"stock": qty}})

# -----------------------
# Get stock for a country
# -----------------------
def get_stock(country):
    country = normalize_country(country)
    s = sessions_col.find_one({"country": country})
    return s.get("stock", 0) if s else 0

# -----------------------
# Set price for country
# -----------------------
def set_price(country, price):
    country = normalize_country(country)
    sessions_col.update_many({"country": country}, {"$set": {"price": price}})

# -----------------------
# Get price for country
# -----------------------
def get_price(country):
    country = normalize_country(country)
    s = sessions_col.find_one({"country": country})
    return s.get("price") if s else None

# -----------------------
# Get country info
# -----------------------
def get_country_info(country):
    country = normalize_country(country)
    return sessions_col.find_one({"country": country})

# -----------------------
# Get all countries
# -----------------------
def get_countries():
    return list(sessions_col.distinct("country"))