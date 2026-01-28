from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.core.client import app
from Nexa.database.sessions import get_available_countries


@app.on_callback_query(filters.regex("^buy_sessions$"))
async def buy_sessions_cb(client, cq):
    await cq.answer()

    countries = get_available_countries()
    if not countries:
        return await cq.message.edit_text("❌ No numbers available right now.")

    buttons = [
        [InlineKeyboardButton(
            f"🌍 {c['country']} — ₹{c['price']}",
            callback_data=f"buy_country:{c['country']}"
        )]
        for c in countries
    ]

    buttons.append([InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")])

    await cq.message.edit_text(
        "🌍 **Select a country**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )