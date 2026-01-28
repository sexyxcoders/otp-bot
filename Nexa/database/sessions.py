from pymongo import MongoClient
from datetime import datetime
import config

client = MongoClient(config.MONGO_URL)
db = client['nexa_bot']
sessions_col = db.sessions

# -----------------------
# Add a session
# -----------------------
def add_session(country: str, price: float, stock: int, string: str, two_step: bool = False, added_by: int = None):
    session = {
        "session_id": string[:10] + str(int(datetime.utcnow().timestamp())),
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
def remove_session(session_id: str):
    sessions_col.delete_one({"session_id": session_id})

# -----------------------
# Revoke a session
# -----------------------
def revoke_session(session_id: str, revoked_by: int = None, revoked_at: datetime = None):
    sessions_col.update_one(
        {"session_id": session_id},
        {"$set": {"revoked": True, "revoked_by": revoked_by, "revoked_at": revoked_at or datetime.utcnow()}}
    )

# -----------------------
# Expire old sessions
# -----------------------
def expire_session(expire_before: datetime):
    sessions_col.update_many(
        {"created_at": {"$lt": expire_before}},
        {"$set": {"revoked": True}}
    )

# -----------------------
# List all sessions
# -----------------------
def list_sessions():
    return list(sessions_col.find())

# -----------------------
# Get session by ID
# -----------------------
def get_session(session_id: str):
    return sessions_col.find_one({"session_id": session_id})

# -----------------------
# Get available session for OTP
# -----------------------
def get_available_session(country: str = None):
    query = {"stock": {"$gt": 0}, "revoked": False}
    if country:
        query["country"] = country
    return sessions_col.find_one(query)

# -----------------------
# Stock management
# -----------------------
def update_stock(country: str, qty: int):
    sessions_col.update_many({"country": country}, {"$inc": {"stock": qty}})

# -----------------------
# Price management
# -----------------------
def set_price(country: str, price: float):
    sessions_col.update_many({"country": country}, {"$set": {"price": price}})

def get_price(country: str):
    s = sessions_col.find_one({"country": country})
    return s.get("price") if s else None

# -----------------------
# Country management
# -----------------------
def add_country(country: str):
    if not sessions_col.find_one({"country": country}):
        sessions_col.insert_one({"country": country, "stock": 0, "price": 0, "string": None, "revoked": False})

def remove_country(country: str):
    sessions_col.delete_many({"country": country})

def get_countries():
    return list(sessions_col.distinct("country"))

def get_country_info(country: str):
    return sessions_col.find_one({"country": country})

# -----------------------
# Assign session to user
# -----------------------
def assign_session_to_user(user_id: int, country: str = None):
    session = get_available_session(country)
    if not session:
        return None
    # Reduce stock
    update_stock(session['country'], -1)
    return session