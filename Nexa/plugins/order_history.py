from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.orders import orders


# ---------------------------
# ORDER HISTORY CALLBACK
# ---------------------------
@app.on_callback_query(filters.regex("^history$|^order_history$"))
async def order_history_cb(client, cq):
    user_id = cq.from_user.id

    # Fetch last 10 orders
    data = list(orders.find({"user_id": user_id}).sort("created_at", -1).limit(10))

    if not data:
        return await cq.message.edit_text(
            "❌ You have no recent orders.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
            ])
        )

    text = "📜 **Your Orders (Last 10)**\n\n"
    for o in data:
        text += f"🌍 {o.get('country', 'N/A')} | 💰 ₹{o.get('price', 0)}\n"

    await cq.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
        ])
    )

    await cq.answer()  # silently acknowledge callback