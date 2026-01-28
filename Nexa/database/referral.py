from Nexa.database.mongo import referrals, users
from datetime import datetime

def add_referral(referrer_id, user_id):
    """
    Save referral relationship.
    """
    # Prevent duplicates
    if referrals.find_one({"user_id": user_id}):
        return False

    referrals.insert_one({
        "user_id": user_id,
        "referrer_id": referrer_id,
        "created_at": datetime.utcnow()
    })
    return True


def get_referrer(user_id):
    """
    Return referrer record for user.
    """
    return referrals.find_one({"user_id": int(user_id)})


def get_referrer_earnings(referrer_id):
    """
    Return total earnings of referrer from user collection.
    """
    user = users.find_one({"user_id": int(referrer_id)})
    return user.get("earnings", 0) if user else 0


def add_earning(referrer_id, amount):
    """
    Add earnings to referrer (5% of deposit).
    """
    users.update_one(
        {"user_id": int(referrer_id)},
        {"$inc": {"earnings": float(amount)}},
        upsert=True
    )


def get_top_referrers(limit=10):
    """
    Top referrers sorted by earnings.
    """
    return list(
        users.find({"earnings": {"$exists": True}})
        .sort("earnings", -1)
        .limit(limit)
    )


def reset_referral_earnings(user_id):
    """
    Reset referrer earnings to zero.
    """
    users.update_one(
        {"user_id": int(user_id)},
        {"$set": {"earnings": 0}}
    )