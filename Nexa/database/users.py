# Nexa/database/users.py
from pymongo import MongoClient
import config
from datetime import datetime

# -----------------------
# MongoDB setup
# -----------------------
client = MongoClient(config.MONGO_URL)
db = client['nexa_bot']
users_col = db.users

# -----------------------
# Ensure user exists
# -----------------------
def ensure_user(user_id, username=None):
    user = users_col.find_one({"user_id": user_id})
    if not user:
        user_data = {
            "user_id": user_id,
            "username": username,
            "balance": 0,
            "created_at": datetime.utcnow(),
        }
        users_col.insert_one(user_data)
        return user_data
    # Update username if changed
    if username and user.get("username") != username:
        users_col.update_one({"user_id": user_id}, {"$set": {"username": username}})
        user["username"] = username
    return user

# -----------------------
# Get user document
# -----------------------
def get_user(user_id):
    return users_col.find_one({"user_id": user_id})

# -----------------------
# Balance management
# -----------------------
def get_balance(user_id):
    user = users_col.find_one({"user_id": user_id})
    return user.get("balance", 0) if user else 0

def add_balance(user_id, amount):
    users_col.update_one({"user_id": user_id}, {"$inc": {"balance": amount}})

def deduct_balance(user_id, amount):
    users_col.update_one({"user_id": user_id}, {"$inc": {"balance": -amount}})

# -----------------------
# Admin check
# -----------------------
def is_admin(user_id):
    return user_id in config.ADMINS

# -----------------------
# Update username
# -----------------------
def update_username(user_id, username):
    users_col.update_one({"user_id": user_id}, {"$set": {"username": username}})

# -----------------------
# Get all users (for broadcast)
# -----------------------
def get_all_users():
    return list(users_col.find())