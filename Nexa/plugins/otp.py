import asyncio
from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Nexa.database.users import get_balance, deduct_balance
from Nexa.database.sessions import (
    get_countries,
    get_available_session,
    mark_session_used,
    get_price
)
from Nexa.database.otp_codes import get_latest_otp, mark_otp_used


# -----------------------
# STEP 1: CLICK GET OTP
# -----------------------
@app.on_callback_query(filters.regex("^get_otp$"))
async def get_otp_cb(client, cq):
    countries = get_countries()

    if not countries:
        return await cq.answer("❌ No country available", show_alert=True)

    buttons = [
        [InlineKeyboardButton(c, callback_data=f"otp_country|{c}")]
        for c in countries
    ]

    await cq.message.edit_text(
        "🌍 **Select Country**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# -----------------------
# STEP 2: SELECT COUNTRY
# -----------------------
@app.on_callback_query(filters.regex("^otp_country\\|"))
async def otp_country_cb(client, cq):
    country = cq.data.split("|")[1]
    price = get_price(country)

    if get_balance(cq.from_user.id) < price:
        return await cq.answer("❌ Insufficient balance", show_alert=True)

    session = get_available_session(country)
    if not session:
        return await cq.answer("❌ Out of stock", show_alert=True)

    deduct_balance(cq.from_user.id, price)
    mark_session_used(session["_id"], cq.from_user.id)

    await cq.message.edit_text(
        f"📱 **Number Assigned**\n\n"
        f"Country: `{country}`\n"
        f"Phone: `{session['phone']}`\n\n"
        f"⏳ Waiting for OTP...",
    )

    # AUTO OTP POLLING
    await poll_otp(cq, session["_id"])


# -----------------------
# STEP 3: AUTO OTP POLLING
# -----------------------
async def poll_otp(cq, session_id):
    for _ in range(30):  # ~60 seconds
        otp = get_latest_otp(session_id)
        if otp:
            mark_otp_used(otp["_id"])
            return await cq.message.edit_text(
                f"✅ **OTP Received**\n\n"
                f"🔐 OTP: `{otp['code']}`",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏠 Main Menu", callback_data="get_otp")]
                ])
            )
        await asyncio.sleep(2)

    await cq.message.edit_text(
        "❌ OTP timeout.\nPlease try again."
    )