from database.mongo import users

# Get user by ID
def get_user(uid):
    return users.find_one({"_id": uid})

# Create new user with 0 balance
def create_user(uid):
    users.insert_one({"_id": uid, "balance": 0})

# Add balance
def add_balance(uid, amount):
    users.update_one({"_id": uid}, {"$inc": {"balance": amount}}, upsert=True)

# Deduct balance
def deduct(uid, amount):
    users.update_one({"_id": uid}, {"$inc": {"balance": -amount}})