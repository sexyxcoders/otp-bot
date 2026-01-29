from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.client import app
from database.users import user_manager

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user = await user_manager.ensure_user(message.from_user.id, message.from_user.username or "")
    
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📩 Get OTP", callback_data="get_otp")],
        [InlineKeyboardButton("💰 My Balance", callback_data="my_balance")],
        [InlineKeyboardButton("📊 My OTPs", callback_data="my_otps")]
    ])
    
    await message.reply_text(
        f"👋 **Welcome to Nexa OTP Bot!**\n\n"
        f"💰 **Balance:** `${user['balance']:.2f}`\n"
        f"📤 Click **Get OTP** for instant SMS delivery!\n\n"
        f"⚡ Fully automated - no manual intervention needed.",
        reply_markup=kb,
        parse_mode="Markdown"
    )