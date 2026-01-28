from Nexa.database.mongo import db
from datetime import datetime

otp_col = db.otp_codes


def store_otp(session_id, code: str):
    otp_col.insert_one({
        "session_id": session_id,
        "code": code,
        "used": False,
        "created_at": datetime.utcnow()
    })


def get_latest_otp(session_id):
    return otp_col.find_one(
        {"session_id": session_id, "used": False},
        sort=[("created_at", -1)]
    )


def mark_otp_used(otp_id):
    otp_col.update_one(
        {"_id": otp_id},
        {"$set": {"used": True}}
    )