from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import get_sessions, revoke_session

@app.on_callback_query(filters.regex("^admin_revoke_session$"))
async def revoke_session_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    sessions = get_sessions()
    buttons = [[InlineKeyboardButton(f"{s['phone']} | {s['country']}", callback_data=f"revoke|{s['_id']}")] for s in sessions]
    await cq.message.edit_text("🛑 **Revoke Session**", reply_markup=InlineKeyboardMarkup(buttons))