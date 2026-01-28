# Nexa/plugins/admin/sessions.py
from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import (
    add_session,
    remove_session,
    revoke_session,
    get_countries,
    get_stock,
    get_price,
    get_country_info,
    update_stock
)

# Temporary state to track admin actions
ADMIN_STATE = {}

# -------------------------------
# Admin Sessions Panel
# -------------------------------
@app.on_callback_query(filters.regex("^admin_sessions$"))
async def admin_sessions_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    countries = get_countries()
    buttons = []

    if countries:
        for country in countries:
            stock = get_stock(country)
            price = get_price(country)
            buttons.append([InlineKeyboardButton(f"{country} | Stock: {stock} | ₹{price}", callback_data=f"admin_sessions_country|{country}")])
    else:
        buttons.append([InlineKeyboardButton("No sessions yet", callback_data="noop")])

    buttons.append([
        InlineKeyboardButton("➕ Add Session", callback_data="admin_add_session"),
        InlineKeyboardButton("🔙 Back", callback_data="admin_panel")
    ])

    await cq.message.edit_text("📲 **Sessions Panel**\nSelect a country or add a session:", reply_markup=InlineKeyboardMarkup(buttons))

# -------------------------------
# Add Session Callback
# -------------------------------
@app.on_callback_query(filters.regex("^admin_add_session$"))
async def admin_add_session_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    ADMIN_STATE[cq.from_user.id] = {"action": "add_session"}
    await cq.message.edit_text(
        "➕ **Add Session**\n\n"
        "Send data in this format:\n"
        "`Country | Price | Stock | SessionString`\n\n"
        "Example:\n"
        "`India | 10 | 1 | abcdef123`",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="admin_panel")]])
    )

# -------------------------------
# Handle Admin Text Input for Adding Session
# -------------------------------
@app.on_message(filters.private & filters.user(lambda uid: uid in ADMIN_STATE))
async def admin_session_input(_, message):
    state = ADMIN_STATE.get(message.from_user.id)
    if not state:
        return

    if state["action"] == "add_session":
        try:
            parts = [p.strip() for p in message.text.split("|")]
            if len(parts) != 4:
                return await message.reply("❌ Format invalid. Use: Country | Price | Stock | SessionString")

            country, price, stock, string = parts
            price = float(price)
            stock = int(stock)

            add_session(country=country, price=price, stock=stock, string=string)
            await message.reply(f"✅ Session added:\nCountry: {country}\nPrice: ₹{price}\nStock: {stock}\nString: {string}")
        except Exception as e:
            await message.reply(f"❌ Error adding session: {e}")

    # Clear admin state
    ADMIN_STATE.pop(message.from_user.id, None)