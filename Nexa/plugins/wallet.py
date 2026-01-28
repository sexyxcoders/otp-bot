from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database import get_user, create_user


# ---------------------------
# WALLET CALLBACK
# ---------------------------
@app.on_callback_query(filters.regex("^wallet$"))
async def wallet_cb(client, cq):
    user_id = cq.from_user.id

    # Get user from DB, create if not exists
    user = get_user(user_id)
    if not user:
        user = create_user(user_id, cq.from_user.username or "")

    balance = user.get("balance", 0)

    text = (
        f"💰 **My Wallet**\n\n"
        f"👤 User: {cq.from_user.mention}\n"
        f"💵 **Balance:** ₹{balance}\n\n"
        "💳 To deposit funds, click Deposit below."
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Deposit", callback_data="deposit")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
    ])

    await cq.message.edit_text(text, reply_markup=keyboard)
    await cq.answer()  # silently acknowledge callback