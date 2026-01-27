from .mongo import db, users
from datetime import datetime
from pymongo import ReturnDocument
import config

deposits = db["deposits"]
counters = db["counters"]
referrals = db["referrals"]  # referral collection


def _get_next_id(name: str):
    counter = counters.find_one_and_update(
        {"_id": name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    if counter is None or "seq" not in counter:
        counters.update_one({"_id": name}, {"$set": {"seq": 1}}, upsert=True)
        return 1

    return counter["seq"]


def add_deposit(user_id, amount, txid=None, proof=None):
    deposit_id = _get_next_id("deposit_id")

    deposit = {
        "id": deposit_id,
        "user_id": int(user_id),
        "amount": int(amount),
        "txid": txid,
        "proof": proof,          # screenshot file_id
        "status": "pending",
        "created_at": datetime.utcnow()
    }

    deposits.insert_one(deposit)
    return deposit


def get_pending_deposits():
    return list(deposits.find({"status": "pending"}).sort("created_at", -1))


def update_deposit_status(deposit_id, status):
    deposit = deposits.find_one_and_update(
        {"id": int(deposit_id)},
        {"$set": {"status": status}},
        return_document=ReturnDocument.AFTER
    )
    return deposit


def get_deposit_by_id(deposit_id):
    return deposits.find_one({"id": int(deposit_id)})


def approve_deposit(deposit_id):
    """
    Approve deposit:
    1. Update status to approved
    2. Add balance to user
    3. Give 5% referral bonus to referrer (if exists)
    """

    deposit = update_deposit_status(deposit_id, "approved")
    if not deposit:
        return None

    # Add deposit amount to user balance
    users.update_one(
        {"user_id": deposit["user_id"]},
        {"$inc": {"balance": deposit["amount"]}},
        upsert=True
    )

    # -------- 5% referral bonus ----------
    ref = referrals.find_one({"user_id": deposit["user_id"]})

    if ref:
        referrer_id = ref["referrer_id"]
        percent = getattr(config, "REFERRAL_PERCENT", 5)
        bonus = int(deposit["amount"] * percent / 100)

        users.update_one(
            {"user_id": referrer_id},
            {"$inc": {"balance": bonus, "earnings": bonus}},
            upsert=True
        )

    return deposit