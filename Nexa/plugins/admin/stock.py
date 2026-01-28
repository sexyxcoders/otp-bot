# Nexa/plugins/admin/stock.py
from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import get_stock, get_countries

@app.on_callback_query(filters.regex("^admin_stock$"))
async def admin_stock_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    countries = get_countries()
    if not countries:
        return await cq.message.edit_text(
            "⚠️ No countries found.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
        )

    # Create buttons for each country with stock displayed
    buttons = []
    for country in countries:
        stock = get_stock(country)
        buttons.append([InlineKeyboardButton(f"{country}: {stock}", callback_data=f"admin_stock_{country}")])

    # Add back button
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="admin_panel")])

    await cq.message.edit_text(
        "📦 **Stock per Country**\nSelect a country to manage:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )