from datetime import datetime, timedelta
import asyncio
from Nexa.database.sessions import (
    assign_session_to_user,
    expire_session,
    mark_session_used,
)
from Nexa.database.otp_codes import (
    store_otp,
    get_latest_otp,
    mark_otp_used
)

# -----------------------
# OTP Polling Interval (seconds)
# -----------------------
OTP_POLL_INTERVAL = 2  # Check every 2 seconds
SESSION_EXPIRE_MINUTES = 10  # Session auto-expire after 10 mins

# -----------------------
# Assign session and start polling OTP
# -----------------------
async def assign_and_poll_otp(user_id: int, country: str = None):
    # 1️⃣ Assign session
    session = assign_session_to_user(user_id, country)
    if not session:
        return None  # No available session

    session_id = session['session_id']
    string_number = session['string']

    # 2️⃣ Start polling for OTP
    otp = None
    start_time = datetime.utcnow()
    expire_time = start_time + timedelta(minutes=SESSION_EXPIRE_MINUTES)

    while datetime.utcnow() < expire_time:
        # Fetch latest OTP for the assigned session
        otp_entry = get_latest_otp(string_number)
        if otp_entry and not otp_entry.get('used', False):
            otp = otp_entry['otp']
            mark_otp_used(otp_entry['id'])  # Mark OTP used
            mark_session_used(session_id)   # Mark session as used
            break
        await asyncio.sleep(OTP_POLL_INTERVAL)

    # 3️⃣ Expire session if not used
    if not otp:
        expire_session(expire_before=start_time)

    return {
        "session_id": session_id,
        "string": string_number,
        "otp": otp
    }

# -----------------------
# Expire all old sessions periodically
# -----------------------
async def expire_old_sessions_task():
    while True:
        expire_time = datetime.utcnow() - timedelta(minutes=SESSION_EXPIRE_MINUTES)
        expire_session(expire_time)
        await asyncio.sleep(60)  # Check every 1 min