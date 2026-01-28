# Nexa/plugins/admin/revoke_session.py
from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import list_sessions, revoke_session

@app.on_callback_query(filters.regex("^admin_revoke_session$"))
async def revoke_session_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    sessions = list_sessions()
    if not sessions:
        return await cq.message.edit_text(
            "🛑 No sessions available to revoke.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
        )

    buttons = [
        [InlineKeyboardButton(f"{s['country']} | {s['string'][:10]} | Stock: {s['stock']}", callback_data=f"revoke|{s['session_id']}")]
        for s in sessions if not s.get("revoked", False)
    ]

    if not buttons:
        buttons = [[InlineKeyboardButton("All sessions already revoked", callback_data="noop")]]

    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="admin_panel")])

    await cq.message.edit_text(
        "🛑 **Revoke Session**\nSelect a session to revoke:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# -------------------------------
# Handle revoke callback
# -------------------------------
@app.on_callback_query(filters.regex(r"^revoke\|(.+)$"))
async def handle_revoke(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    session_id = cq.data.split("|")[1]
    revoke_session(session_id)
    await cq.answer("✅ Session revoked", show_alert=True)

    # Refresh the revoke panel
    await revoke_session_cb(_, cq)