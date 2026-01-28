from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import set_price, get_countries, get_price

@app.on_callback_query(filters.regex("^admin_prices$"))
async def prices_panel(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    buttons = []
    for c in get_countries():
        price = get_price(c)
        buttons.append([
            InlineKeyboardButton(f"{c}: ₹{price}", callback_data=f"set_price|{c}")
        ])
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="admin_panel")])

    await cq.message.edit_text(
        "💰 **Set / Update Price**\nSelect country to set price:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex(r"^set_price\|(.+)$"))
async def set_price_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    country = cq.data.split("|")[1]
    new_price = 10  # Example price, replace with input system if desired
    set_price(country, new_price)
    await cq.answer(f"✅ Price for {country} set to ₹{new_price}", show_alert=True)
    await prices_panel(_, cq)