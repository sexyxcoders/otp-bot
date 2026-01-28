import asyncio
from datetime import datetime, timedelta
from Nexa.database.sessions import get_session, assign_session_to_user, expire_session, update_stock
from Nexa.database.otp_codes import store_otp, get_latest_otp, mark_otp_used
from Nexa.database.users import deduct_balance

OTP_EXPIRE_MINUTES = 5

async def assign_and_poll_otp(user_id, country):
    # 1️⃣ Assign available session
    session = assign_session_to_user(user_id, country)
    if not session:
        return None, "❌ No session available"

    session_id = session['session_id']
    price = session['price']

    # Deduct user balance
    deduct_balance(user_id, price)

    # 2️⃣ Poll OTP every 2s (simulate)
    for _ in range(60):  # max 2 minutes
        otp_record = get_latest_otp(session_id)
        if otp_record and not otp_record.get("used"):
            # Mark OTP as used
            mark_otp_used(session_id, otp_record['otp'])
            return otp_record['otp'], session['string']
        await asyncio.sleep(2)

    # 3️⃣ If OTP not received, expire session for this user
    expire_session(session_id)
    update_stock(country, -1)
    return None, "❌ OTP timed out"