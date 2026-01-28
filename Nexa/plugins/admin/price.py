from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import get_countries, get_price

@app.on_callback_query(filters.regex("^admin_prices$"))
async def admin_prices_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    countries = get_countries()
    text = "💰 **Price Management**\n\n"
    for c in countries:
        price = get_price(c)
        text += f"• {c}: ₹{price if price else 'Not set'}\n"
    text += "\nUse /setprice [country] [amount]"
    await cq.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]]))