from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import add_country, remove_country, get_countries

@app.on_callback_query(filters.regex("^add_country$"))
async def add_country_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)
    countries = get_countries()
    text = "🌍 **Add Country**\n\n"
    text += "Current Countries:\n" + "\n".join(countries) if countries else "No countries yet."
    text += "\n\nUse /addcountry [name] to add."
    await cq.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]]))

@app.on_callback_query(filters.regex("^remove_country$"))
async def remove_country_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)
    countries = get_countries()
    text = "❌ **Remove Country**\n\n"
    text += "Current Countries:\n" + "\n".join(countries) if countries else "No countries yet."
    text += "\n\nUse /removecountry [name] to remove."
    await cq.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]]))