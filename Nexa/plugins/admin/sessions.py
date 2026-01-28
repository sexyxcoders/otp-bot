from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import add_session, remove_session, get_countries

@app.on_callback_query(filters.regex("^admin_sessions$"))
async def admin_sessions_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    countries = get_countries()
    text = "📲 **Sessions**\n\n"
    text += "\n".join(countries) if countries else "No sessions yet."
    await cq.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]]))