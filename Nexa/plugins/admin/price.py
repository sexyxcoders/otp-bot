from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import set_price, get_countries, get_price


@app.on_callback_query(filters.regex("^admin_prices$"))
async def admin_prices_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    countries = get_countries()
    text = "💰 **Price Management**\n\n"

    if not countries:
        text += "No countries added yet."
    else:
        for c in countries:
            name = c.get("name", "Unknown")
            price = get_price(name)
            price_text = f"₹{price}" if price else "Not set"
            text += f"• **{name}**: {price_text}\n"

    text += "\nTo change price use:\n`/setprice [country] [amount]`"

    await cq.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )


@app.on_message(filters.command("setprice"))
async def set_price_cmd(_, msg):
    if not is_admin(msg.from_user.id):
        return

    try:
        _, country, price = msg.text.split()
        set_price(country, float(price))
        await msg.reply(f"💰 Price for {country} set to {price}")
    except ValueError:
        await msg.reply("❌ Usage: `/setprice [country] [amount]`")