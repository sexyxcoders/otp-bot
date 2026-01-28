from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.orders import orders

@app.on_callback_query(filters.regex("^order_history$"))
async def order_history(client, callback):
    user_id = callback.from_user.id
    data = list(orders.find({"user_id": user_id}).sort("created_at", -1).limit(10))

    if not data:
        return await callback.message.edit_text("❌ No orders found")

    text = "📜 **Your Orders**\n\n"
    for o in data:
        text += f"🌍 {o['country']} | ₹{o['price']}\n"

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
        ])
    )