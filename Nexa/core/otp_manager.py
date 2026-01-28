import asyncio
from datetime import datetime, timedelta

from Nexa.database.sessions import (
    get_available_session,
    mark_session_used,
    expire_session
)
from Nexa.database.otp_codes import (
    store_otp,
    get_latest_otp,
    mark_otp_used
)
from Nexa.database.users import deduct_balance
from Nexa.core.client import app


OTP_TIMEOUT = 120  # seconds (2 min)


async def assign_session_and_wait_otp(user_id: int, country: str, price: int):
    """
    1️⃣ Assign available session
    2️⃣ Deduct balance
    3️⃣ Poll OTP automatically
    4️⃣ Expire session after use
    """

    # 🔎 Get free session
    session = get_available_session(country)
    if not session:
        return None, "❌ No stock available"

    # 💰 Deduct balance
    if not deduct_balance(user_id, price):
        return None, "❌ Insufficient balance"

    session_id = session["session_id"]
    phone = session["phone"]

    # 🔐 Lock session
    mark_session_used(session_id, user_id)

    # ⏳ OTP polling
    start_time = datetime.utcnow()

    while True:
        otp = get_latest_otp(session_id)
        if otp:
            mark_otp_used(otp["_id"])
            expire_session(session_id)
            return otp["code"], phone

        if datetime.utcnow() - start_time > timedelta(seconds=OTP_TIMEOUT):
            expire_session(session_id)
            return None, "⌛ OTP timeout"

        await asyncio.sleep(3)