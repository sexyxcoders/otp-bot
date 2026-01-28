from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Nexa.database.users import is_admin
from Nexa.database.sessions import (
    get_countries,
    get_price,
    set_price
)

# 🔹 MAIN PRICE PANEL
@app.on_callback_query(filters.regex("^admin_prices$"))
async def admin_prices(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    countries = get_countries()
    text = "💰 **Price Management**\n\n"

    buttons = []

    if not countries:
        text += "⚠️ No countries added yet."
    else:
        for c in countries:
            name = c["name"]
            price = get_price(name)
            price_text = f"₹{price}" if price else "Not set"

            text += f"• **{name}** → {price_text}\n"

            buttons.append([
                InlineKeyboardButton(
                    f"✏️ Set {name} Price",
                    callback_data=f"setprice:{name}"
                )
            ])

    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="admin_panel")])

    await cq.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# 🔹 ASK PRICE INPUT
@app.on_callback_query(filters.regex("^setprice:"))
async def ask_price(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    country = cq.data.split(":", 1)[1]

    await cq.message.edit_text(
        f"💰 **Set Price**\n\n"
        f"Country: **{country}**\n\n"
        f"Send price now (numbers only):",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="admin_prices")]
        ])
    )

    # save temp state
    app.price_state[cq.from_user.id] = country


# 🔹 RECEIVE PRICE VALUE
@app.on_message(filters.private & filters.text)
async def receive_price(_, msg):
    uid = msg.from_user.id

    if uid not in getattr(app, "price_state", {}):
        return

    if not is_admin(uid):
        return

    country = app.price_state.pop(uid)

    try:
        price = float(msg.text)
    except ValueError:
        return await msg.reply("❌ Invalid price. Send number only.")

    set_price(country, price)

    await msg.reply(
        f"✅ **Price Updated**\n\n"
        f"🌍 Country: **{country}**\n"
        f"💰 Price: ₹{price}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Prices", callback_data="admin_prices")]
        ])
    )