# Nexa/database/deposits.py
from datetime import datetime
from .mongo import db  # Use the shared Mongo connection

deposits_col = db.deposits


# -----------------------
# Add a new deposit
# -----------------------
def add_deposit(user_id: int, amount: float, txid: str = None):
    deposit = {
        "id": int(datetime.utcnow().timestamp() * 1000),  # unique ID based on timestamp
        "user_id": user_id,
        "amount": amount,
        "txid": txid,
        "status": "pending",  # pending, approved, rejected, expired
        "created_at": datetime.utcnow()
    }
    deposits_col.insert_one(deposit)
    return deposit


# -----------------------
# Get deposit by ID
# -----------------------
def get_deposit_by_id(deposit_id: int):
    return deposits_col.find_one({"id": deposit_id})


# -----------------------
# Get all pending deposits
# -----------------------
def get_pending_deposits():
    return list(deposits_col.find({"status": "pending"}).sort("created_at", -1))


# -----------------------
# Update deposit status
# -----------------------
def update_deposit_status(deposit_id: int, status: str):
    deposits_col.update_one(
        {"id": deposit_id},
        {"$set": {"status": status, "processed_at": datetime.utcnow()}}
    )


# -----------------------
# Approve a deposit
# -----------------------
def approve_deposit(deposit_id: int):
    dep = get_deposit_by_id(deposit_id)
    if not dep or dep.get("status") != "pending":
        return False

    from .users import add_balance

    # Update deposit status
    update_deposit_status(deposit_id, "approved")

    # Add balance to user
    add_balance(dep["user_id"], dep["amount"])
    return True


# -----------------------
# Expire old deposits (optional utility)
# -----------------------
def expire_old_deposits(minutes: int = 10):
    from datetime import timedelta
    cutoff = datetime.utcnow() - timedelta(minutes=minutes)
    deposits_col.update_many(
        {"status": "pending", "created_at": {"$lt": cutoff}},
        {"$set": {"status": "expired"}}
    )