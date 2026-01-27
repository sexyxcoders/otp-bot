from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database import get_total_orders, create_user, get_user


def profile_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ])


@Client.on_callback_query(filters.regex("^profile$"))
async def profile_cb(client, callback_query):
    user = callback_query.from_user

    user_id = user.id
    name = user.first_name or "No Name"
    username = f"@{user.username}" if user.username else "No Username"

    # create user if not exists
    create_user(user_id, user.username)

    user_data = get_user(user_id)
    balance = user_data.get("balance", 0) if user_data else 0
    orders = get_total_orders(user_id)

    text = (
        "👤 **Your Profile**\n\n"
        f"🆔 **User ID:** `{user_id}`\n"
        f"👤 **Name:** {name}\n"
        f"🔖 **Username:** {username}\n"
        f"💰 **Balance:** ₹{balance}\n"
        f"📦 **Total Orders:** {orders}"
    )

    await callback_query.message.edit_text(
        text,
        reply_markup=profile_keyboard()
    )