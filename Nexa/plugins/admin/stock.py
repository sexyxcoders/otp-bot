from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import get_stock, get_countries

@app.on_callback_query(filters.regex("^admin_stock$"))
async def admin_stock_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    text = "📦 **Stock per country**\n\n"
    for c in get_countries():
        text += f"{c}: {get_stock(c)}\n"
    await cq.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]]))