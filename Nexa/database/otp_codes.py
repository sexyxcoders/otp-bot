from Nexa.database.mongo import otp_codes
from datetime import datetime, timedelta


def store_otp(session_id, user_id, otp_code, ttl_min=5):
    otp_codes.insert_one({
        "session_id": session_id,
        "user_id": user_id,
        "otp_code": otp_code,
        "status": "unused",
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(minutes=ttl_min)
    })


def get_latest_otp(session_id):
    return otp_codes.find_one(
        {
            "session_id": session_id,
            "status": "unused",
            "expires_at": {"$gt": datetime.utcnow()}
        },
        sort=[("created_at", -1)]
    )


def mark_otp_used(otp_id):
    otp_codes.update_one(
        {"_id": otp_id},
        {"$set": {
            "status": "used",
            "used_at": datetime.utcnow()
        }}
    )