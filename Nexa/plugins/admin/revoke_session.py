from datetime import datetime

from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Nexa.database.users import is_admin
from Nexa.database.sessions import revoke_session, get_session

# temporary admin state
REVOKE_STATE = {}


# ---------- BUTTON ----------
@app.on_callback_query(filters.regex("^admin_revoke_session$"))
async def admin_revoke_btn(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    REVOKE_STATE[cq.from_user.id] = True

    await cq.message.edit_text(
        "🛑 **Revoke Session**\n\n"
        "Send the **Session ID** you want to revoke.\n\n"
        "Example:\n`abc123xyz`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
        ])
    )


# ---------- INPUT HANDLER ----------
@app.on_message(filters.private)
async def revoke_input_handler(_, msg):
    if msg.from_user.id not in REVOKE_STATE:
        return

    if not is_admin(msg.from_user.id):
        REVOKE_STATE.pop(msg.from_user.id, None)
        return

    session_id = msg.text.strip()
    REVOKE_STATE.pop(msg.from_user.id, None)

    session = get_session(session_id)

    if not session:
        return await msg.reply("❌ Session not found.")

    if session.get("revoked"):
        return await msg.reply("⚠️ Session already revoked.")

    revoke_session(
        session_id=session_id,
        revoked_by=msg.from_user.id,
        revoked_at=datetime.utcnow()
    )

    await msg.reply(
        f"🛑 **Session Revoked Successfully**\n\n"
        f"🆔 `{session_id}`\n"
        f"🌍 {session.get('country')}\n"
        f"👤 Admin: `{msg.from_user.id}`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Admin Panel", callback_data="admin_panel")]
        ])
    )