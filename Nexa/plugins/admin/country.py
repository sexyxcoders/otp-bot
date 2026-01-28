from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import add_country, get_countries

# ----------------------
# INLINE ADD COUNTRY MENU
# ----------------------
@app.on_callback_query(filters.regex("^add_country$"))
async def add_country_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    countries = ["India", "USA", "UK", "Germany", "France", "Japan", "Australia"]  # You can change default list
    text = "➕ **Add Country**\n\nSelect a country to add:"

    buttons = []
    for c in countries:
        buttons.append([InlineKeyboardButton(c, callback_data=f"add_country_now|{c}")])
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="admin_panel")])

    await cq.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))


# ----------------------
# ADD COUNTRY INLINE ACTION
# ----------------------
@app.on_callback_query(filters.regex(r"^add_country_now\|(.+)$"))
async def add_country_now_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    country = cq.data.split("|")[1]

    # Check if already exists
    existing = [c["name"] for c in get_countries()]
    if country in existing:
        return await cq.answer(f"⚠️ Country **{country}** already added", show_alert=True)

    add_country(country)
    await cq.answer(f"✅ Country **{country}** added", show_alert=True)

    # Update message to reflect success
    await cq.message.edit_text(
        f"✅ Country **{country}** added successfully.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )