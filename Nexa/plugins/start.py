from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import ensure_user


@app.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    ensure_user(
        user_id=message.from_user.id,
        username=message.from_user.username
    )

    await message.reply_text(
        "👋 **Welcome to OTP Service Bot**\n\n"
        "• Auto number assign\n"
        "• Auto OTP fetch\n"
        "• Fast & Secure\n\n"
        "Click below 👇",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 Get OTP", callback_data="get_otp")]
        ])
    )