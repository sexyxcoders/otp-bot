from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database import create_user, get_user, get_total_orders


# ---------------------------
# PROFILE KEYBOARD
# ---------------------------
def profile_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
    ])


# ---------------------------
# PROFILE CALLBACK
# ---------------------------
@app.on_callback_query(filters.regex("^profile$"))
async def profile_cb(client, cq):
    user = cq.from_user
    user_id = user.id

    # Create user if not exists
    create_user(user_id, user.username or "")

    # Fetch user data
    user_data = get_user(user_id)
    balance = user_data.get("balance", 0) if user_data else 0
    orders = get_total_orders(user_id)

    name = user.first_name or "No Name"
    username = f"@{user.username}" if user.username else "No Username"

    text = (
        "👤 **Your Profile**\n\n"
        f"🆔 **User ID:** `{user_id}`\n"
        f"👤 **Name:** {name}\n"
        f"🔖 **Username:** {username}\n"
        f"💰 **Balance:** ₹{balance}\n"
        f"📦 **Total Orders:** {orders}"
    )

    await cq.message.edit_text(text, reply_markup=profile_keyboard())
    await cq.answer()  # silently acknowledge callback