"""
OTP Watcher Worker
------------------
• Listens to incoming messages on sold sessions
• Extracts OTP automatically
• Stores OTP securely
• Auto-expire session after use
"""

from pyrogram import filters
from pyrogram.types import Message
from datetime import datetime, timedelta
import re

from Nexa.core.client import app
from Nexa.database.sessions import sessions, expire_session
from Nexa.database.otp_codes import store_otp


def is_session_valid(session):
    if not session:
        return False
    if not session.get("active"):
        return False
    if session.get("revoked"):
        return False
    if session.get("expires_at") and session["expires_at"] < datetime.utcnow():
        return False
    return True


def extract_otp(text):
    if not text:
        return None
    match = re.search(r'\b(\d{4,8})\b', text)
    return match.group(1) if match else None


def get_active_session_by_chat(chat_id):
    return sessions.find_one({
        "user_id": chat_id,
        "sold": True,
        "active": True,
        "revoked": False
    })


@app.on_message(filters.private & filters.text, group=10)
async def otp_watcher(client, message: Message):
    """
    Triggered on ALL incoming messages.
    Filters only OTP-related messages automatically.
    """

    # Ignore bot messages
    if message.from_user and message.from_user.is_bot:
        return

    chat_id = message.chat.id
    text = message.text or ""

    # 🔍 Find active session linked to this chat
    session = get_active_session_by_chat(chat_id)
    if not is_session_valid(session):
        return

    # 🔐 Extract OTP
    otp_code = extract_otp(text)
    if not otp_code:
        return

    # 💾 Save OTP
    store_otp(
        session_id=session["_id"],
        user_id=session["user_id"],
        otp_code=otp_code
    )

    # 🔥 OPTIONAL: Auto-expire session after OTP
    if session.get("auto_expire", True):
        expire_session(session["_id"])

    print(
        f"[OTP] Captured OTP {otp_code} "
        f"for session {session['_id']}"
    )