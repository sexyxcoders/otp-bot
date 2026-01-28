from pyrogram import filters
from Nexa.core.client import app
from Nexa.database.sessions import get_session
from Nexa.database.otp_codes import get_latest_otp
from Nexa.utils.otp_validator import is_session_valid
from Nexa.plugins.sessions.otp_ui import otp_keyboard


@app.on_callback_query(filters.regex("^get_otp:"))
async def get_otp_cb(client, cq):
    await cq.answer()

    session_id = cq.data.split(":")[1]
    user_id = cq.from_user.id

    session = get_session(session_id)
    if not session or session["user_id"] != user_id:
        return await cq.message.reply("❌ Invalid session.")

    if not is_session_valid(session):
        return await cq.message.reply("⛔ Session expired or revoked.")

    otp = get_latest_otp(session_id)
    if not otp:
        return await cq.message.reply("⌛ Waiting for OTP...")

    await cq.message.reply(
        f"🔐 **OTP Code**\n\n"
        f"`{otp['otp_code']}`\n"
        f"⏳ Expires soon",
        reply_markup=otp_keyboard(session_id)
    )