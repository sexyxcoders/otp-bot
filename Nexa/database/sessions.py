from pymongo import MongoClient
from datetime import datetime
import config

client = MongoClient(config.MONGO_URL)
db = client['nexa_bot']

sessions_col = db.sessions

# -----------------------
# Add country session
# -----------------------
def add_country(country):
    if not sessions_col.find_one({"country": country}):
        sessions_col.insert_one({
            "country": country,
            "price": 0,
            "stock": 0,
            "sessions": [],
            "created_at": datetime.utcnow()
        })

def remove_country(country):
    sessions_col.delete_many({"country": country})

def set_price(country, price):
    sessions_col.update_many({"country": country}, {"$set": {"price": price}})

def get_price(country):
    c = sessions_col.find_one({"country": country})
    return c.get("price") if c else None

def get_countries():
    return [c["country"] for c in sessions_col.find()]

def get_available_countries():
    return get_countries()

# -----------------------
# Add session string + stock
# -----------------------
def add_session(country, string, stock=1):
    session = {
        "session_id": string[:10] + str(datetime.utcnow().timestamp()),
        "string": string,
        "stock": stock,
        "assigned_to": None,
        "revoked": False,
        "created_at": datetime.utcnow()
    }
    sessions_col.update_one({"country": country}, {"$push": {"sessions": session}})
    return session

def remove_session(session_id):
    sessions_col.update_many({}, {"$pull": {"sessions": {"session_id": session_id}}})

def revoke_session(session_id):
    sessions_col.update_many(
        {"sessions.session_id": session_id},
        {"$set": {"sessions.$.revoked": True}}
    )

# -----------------------
# Assign session to user automatically
# -----------------------
def assign_session_to_user(user_id, country):
    country_doc = sessions_col.find_one({"country": country})
    if not country_doc:
        return None

    for sess in country_doc["sessions"]:
        if sess["assigned_to"] is None and sess["stock"] > 0 and not sess["revoked"]:
            # Assign session
            sess["assigned_to"] = user_id
            sess["assigned_at"] = datetime.utcnow()
            sessions_col.update_one(
                {"country": country, "sessions.session_id": sess["session_id"]},
                {"$set": sess}
            )
            return sess
    return None

# -----------------------
# Expire session for user
# -----------------------
def expire_session(session_id):
    sessions_col.update_many(
        {"sessions.session_id": session_id},
        {"$set": {"sessions.$.assigned_to": None, "sessions.$.assigned_at": None}}
    )

# -----------------------
# Update stock
# -----------------------
def update_stock(country, qty):
    # update first available session stock
    sessions_col.update_one(
        {"country": country, "sessions.stock": {"$gt": 0}},
        {"$inc": {"sessions.$.stock": qty}}
    )

# -----------------------
# Get session by ID
# -----------------------
def get_session(session_id):
    return sessions_col.find_one({"sessions.session_id": session_id}, {"sessions.$": 1})