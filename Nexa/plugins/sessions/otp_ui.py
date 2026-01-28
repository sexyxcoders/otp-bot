from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def otp_keyboard(session_id: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "🔄 Refresh OTP",
            callback_data=f"get_otp:{session_id}"
        )],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
    ])