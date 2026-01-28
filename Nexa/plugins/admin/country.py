from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import add_country, remove_country, get_countries

# -------------------------------
# Open country panel
# -------------------------------
@app.on_callback_query(filters.regex("^admin_countries$"))
async def countries_panel(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    buttons = []
    for c in get_countries():
        buttons.append([
            InlineKeyboardButton(f"❌ {c}", callback_data=f"remove_country|{c}")
        ])
    buttons.append([InlineKeyboardButton("➕ Add Country", callback_data="add_country")])
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="admin_panel")])

    await cq.message.edit_text(
        "🌍 **Countries Management**\nSelect a country to remove or add new:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# -------------------------------
# Add country callback
# -------------------------------
@app.on_callback_query(filters.regex(r"^add_country$"))
async def add_country_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    # Here we just simulate: you can later add a text prompt if needed
    country_name = "India"  # Default example, replace with input system if you want
    add_country(country_name)
    await cq.answer(f"✅ Country {country_name} added", show_alert=True)
    await countries_panel(_, cq)

# -------------------------------
# Remove country callback
# -------------------------------
@app.on_callback_query(filters.regex(r"^remove_country\|(.+)$"))
async def remove_country_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    country = cq.data.split("|")[1]
    remove_country(country)
    await cq.answer(f"❌ Country {country} removed", show_alert=True)
    await countries_panel(_, cq)