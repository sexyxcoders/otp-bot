from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
import config

from Nexa.database import (
    create_user, update_username, get_available_countries,
    get_balance, get_total_orders, get_referrer_earnings, is_admin
)


# ---------------------------
# KEYBOARD HELPERS
# ---------------------------
def start_keyboard(user_id=None):
    keyboard = [
        [InlineKeyboardButton("📲 Buy Number", callback_data="buy_sessions")],
        [
            InlineKeyboardButton("👤 Profile", callback_data="profile"),
            InlineKeyboardButton("💰 Wallet", callback_data="wallet")
        ],
        [
            InlineKeyboardButton("💳 Deposit", callback_data="deposit"),
            InlineKeyboardButton("📜 History", callback_data="history")
        ],
        [
            InlineKeyboardButton("🎁 Refer & Earn", callback_data="refer"),
            InlineKeyboardButton("🧑‍💻 Support", callback_data="support")
        ]
    ]

    # Admin panel
    if user_id and is_admin(user_id):
        keyboard.append([InlineKeyboardButton("👑 Admin Panel", callback_data="admin_panel")])

    return InlineKeyboardMarkup(keyboard)


# ---------------------------
# MUST JOIN CHECK
# ---------------------------
async def must_join(client, user_id, chat_id, edit_msg=None):
    if not getattr(config, "MUST_JOIN", None):
        return True

    try:
        await client.get_chat_member(config.MUST_JOIN, user_id)
        return True
    except UserNotParticipant:
        text = "⚠️ **You must join our channel to use this bot**"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{config.MUST_JOIN}")],
            [InlineKeyboardButton("✅ Joined", callback_data="check_join")]
        ])
        if edit_msg:
            await edit_msg.edit_text(text, reply_markup=keyboard)
        else:
            await client.send_message(chat_id, text, reply_markup=keyboard)
        return False


# ---------------------------
# START COMMAND
# ---------------------------
@app.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    user = message.from_user

    # Must join check
    if not await must_join(client, user.id, message.chat.id):
        return

    # Create / update user
    create_user(user.id, user.username or "")
    update_username(user.id, user.username or "")

    keyboard = start_keyboard(user.id)
    await message.reply_text(
        "✨ **Welcome to Nexa Number Market**\n\n"
        "Buy virtual numbers instantly at best prices 🚀\n\n"
        "Select an option below 👇",
        reply_markup=keyboard
    )


# ---------------------------
# CHECK JOIN BUTTON
# ---------------------------
@app.on_callback_query(filters.regex("^check_join$"))
async def check_join_cb(client, cq):
    await cq.answer()
    if not await must_join(client, cq.from_user.id, cq.message.chat.id, edit_msg=cq.message):
        return

    await cq.message.edit_text(
        "✅ **Access granted!**\n\nChoose an option below 👇",
        reply_markup=start_keyboard(cq.from_user.id)
    )


# ---------------------------
# MAIN MENU BUTTON
# ---------------------------
@app.on_callback_query(filters.regex("^main_menu$"))
async def main_menu_cb(client, cq):
    await cq.answer()
    await cq.message.edit_text(
        "✨ **Welcome to Nexa Number Market**\n\nSelect an option below 👇",
        reply_markup=start_keyboard(cq.from_user.id)
    )