from pymongo import MongoClient
from datetime import datetime, timedelta
import config

client = MongoClient(config.MONGO_URL)
db = client['nexa_bot']

otp_col = db.otp_codes

OTP_EXPIRE_MINUTES = 5

# -----------------------
# Store OTP for a session
# -----------------------
def store_otp(session_id, otp):
    otp_col.insert_one({
        "session_id": session_id,
        "otp": otp,
        "used": False,
        "created_at": datetime.utcnow()
    })

# -----------------------
# Get latest OTP for session
# -----------------------
def get_latest_otp(session_id):
    return otp_col.find_one(
        {"session_id": session_id, "used": False},
        sort=[("created_at", -1)]
    )

# -----------------------
# Mark OTP as used
# -----------------------
def mark_otp_used(session_id, otp):
    otp_col.update_one(
        {"session_id": session_id, "otp": otp},
        {"$set": {"used": True}}
    )

# -----------------------
# Expire OTP older than X minutes
# -----------------------
def expire_otps():
    expire_time = datetime.utcnow() - timedelta(minutes=OTP_EXPIRE_MINUTES)
    otp_col.update_many(
        {"used": False, "created_at": {"$lt": expire_time}},
        {"$set": {"used": True}}
    )