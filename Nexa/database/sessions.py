# Nexa/database/sessions.py
from datetime import datetime

# If you use MongoDB, replace this list with proper collection calls
sessions_db = []  # List of all sessions
countries_db = []  # List of countries


# -----------------------------
# Country Management
# -----------------------------
def add_country(name):
    name = name.strip()
    if name not in countries_db:
        countries_db.append({"name": name})


def remove_country(name):
    global countries_db
    countries_db = [c for c in countries_db if c["name"] != name]


def get_countries():
    return countries_db


# -----------------------------
# Session Management
# -----------------------------
def add_session(country, price, stock, string_session, two_step=False, added_by=None):
    session_id = len(sessions_db) + 1
    sessions_db.append({
        "id": session_id,
        "country": country,
        "price": price,
        "stock": stock,
        "session": string_session,
        "two_step": two_step,
        "added_by": added_by,
        "revoked": False,
        "created_at": datetime.utcnow()
    })
    return session_id


def remove_session(session_id):
    global sessions_db
    sessions_db = [s for s in sessions_db if str(s["id"]) != str(session_id)]


def get_session(session_id):
    for s in sessions_db:
        if str(s["id"]) == str(session_id):
            return s
    return None


def list_sessions():
    return sessions_db


def revoke_session(session_id, revoked_by=None, revoked_at=None):
    s = get_session(session_id)
    if s:
        s["revoked"] = True
        s["revoked_by"] = revoked_by
        s["revoked_at"] = revoked_at or datetime.utcnow()
        return True
    return False


# -----------------------------
# Stock Management
# -----------------------------
def update_stock(country, qty_change):
    for s in sessions_db:
        if s["country"] == country:
            s["stock"] += qty_change
            if s["stock"] < 0:
                s["stock"] = 0


# -----------------------------
# Price Management
# -----------------------------
def set_price(country, price):
    for s in sessions_db:
        if s["country"] == country:
            s["price"] = price


def get_price(country):
    for s in sessions_db:
        if s["country"] == country:
            return s.get("price", None)
    return None