from datetime import datetime
from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import get_active_sessions, revoke_session

# 🔘 SHOW SESSIONS WITH REVOKE BUTTON
@app.on_callback_query(filters.regex("^admin_revoke_session$"))
async def admin_revoke_session_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    sessions = get_active_sessions()  # fetch all active sessions
    if not sessions:
        return await cq.message.edit_text(
            "⚠️ No active sessions found.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
        )

    keyboard = []
    for s in sessions:
        # each button text = session_id | country
        # callback_data = revoke:<session_id>
        keyboard.append([
            InlineKeyboardButton(f"{s['session_id']} | {s['country']}", callback_data=f"revoke_{s['session_id']}")
        ])

    # Add back button at bottom
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="admin_panel")])

    await cq.message.edit_text(
        "🛑 **Active Sessions**\n\nClick a session to revoke it:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    await cq.answer()


# 🔘 HANDLE REVOKE CLICK
@app.on_callback_query(filters.regex(r"^revoke_(.+)$"))
async def handle_revoke_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    session_id = cq.data.split("_", 1)[1]
    session = get_active_sessions(session_id)  # check if session exists

    if not session:
        return await cq.answer("❌ Session not found.", show_alert=True)

    revoke_session(session_id=session_id, revoked_by=cq.from_user.id, revoked_at=datetime.utcnow())
    await cq.answer(f"✅ Session {session_id} revoked.", show_alert=True)

    # Refresh the list after revoking
    await admin_revoke_session_cb(_, cq)