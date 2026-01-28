from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.core.client import app
from Nexa.database.sessions import get_country_info


@app.on_callback_query(filters.regex("^buy_country:"))
async def country_cb(client, cq):
    await cq.answer()

    country = cq.data.split(":")[1]
    info = get_country_info(country)

    if not info:
        return await cq.message.reply("❌ Country unavailable.")

    await cq.message.edit_text(
        f"🌍 **{country} Number**\n\n"
        f"💰 Price: ₹{info['price']}\n"
        f"📦 Stock: {info['stock']}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Buy", callback_data=f"confirm_buy:{country}")],
            [InlineKeyboardButton("🔙 Back", callback_data="buy_sessions")]
        ])
    )