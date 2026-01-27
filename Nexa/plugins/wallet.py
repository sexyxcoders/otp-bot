from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database import get_user, create_user


@app.on_callback_query(filters.regex("^wallet$"))
async def wallet_cb(client, callback_query):
    user_id = callback_query.from_user.id

    # create user if not exists
    user = get_user(user_id)
    if not user:
        user = create_user(user_id, callback_query.from_user.username)

    balance = user.get("balance", 0)

    await callback_query.message.edit_text(
        f"💰 **Your Wallet**\n\n"
        f"💵 **Balance:** ₹{balance}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
        ])
    )