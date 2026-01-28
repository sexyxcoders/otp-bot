# Nexa/database/sessions.py
from pymongo import MongoClient
from datetime import datetime
import config

# -----------------------
# MongoDB Setup
# -----------------------
client = MongoClient(config.MONGO_URL)
db = client['nexa_bot']
sessions_col = db.sessions

# -----------------------
# Helper: Normalize country name
# -----------------------
def normalize_country(country_name: str) -> str:
    """
    Normalize country name for consistent storage:
    - Strip spaces
    - Capitalize each word
    """
    if not country_name:
        return ""
    return " ".join(word.capitalize() for word in country_name.strip().split())

# -----------------------
# Country Management
# -----------------------
def add_country(country_name: str):
    country_name = normalize_country(country_name)
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

def remove_country(country_name: str):
    country_name = normalize_country(country_name)
    sessions_col.delete_many({"country": country_name})

def get_countries() -> list:
    """Return a list of all country names"""
    return sessions_col.distinct("country")

def get_available_countries() -> list:
    """Return countries that have active sessions"""
    return sessions_col.distinct("country", {"revoked": False})

def get_country_info(country_name: str) -> dict:
    country_name = normalize_country(country_name)
    return sessions_col.find_one({"country": country_name})

# -----------------------
# Session Management
# -----------------------
def add_session(country: str, price: float, stock: int, string: str, two_step=False, added_by=None):
    country = normalize_country(country)
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

def remove_session(session_id: str):
    sessions_col.delete_one({"session_id": session_id})

def revoke_session(session_id: str, revoked_by=None, revoked_at=None):
    sessions_col.update_one(
        {"session_id": session_id},
        {"$set": {"revoked": True, "revoked_by": revoked_by, "revoked_at": revoked_at}}
    )

def list_sessions() -> list:
    return list(sessions_col.find())

def get_session(session_id: str) -> dict:
    return sessions_col.find_one({"session_id": session_id})

# -----------------------
# Stock Management
# -----------------------
def update_stock(country: str, qty: int):
    country = normalize_country(country)
    sessions_col.update_many({"country": country}, {"$inc": {"stock": qty}})

# -----------------------
# Price Management
# -----------------------
def set_price(country: str, price: float):
    country = normalize_country(country)
    sessions_col.update_many({"country": country}, {"$set": {"price": price}})

def get_price(country: str) -> float:
    country = normalize_country(country)
    s = sessions_col.find_one({"country": country})
    return s.get("price") if s else None