from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def deliver_session(client, message, session):
    text = (
        "📞 **Your Number is Ready**\n\n"
        f"🌍 Country: {session['country']}\n"
        f"📱 Number: `{session['number']}`\n\n"
        "🔐 **Login Instructions**:\n"
        "1. Open Telegram\n"
        "2. Enter number\n"
        "3. Click **Get OTP** below\n\n"
        "⏳ Valid for limited time"
    )

    if session.get("two_step"):
        text += f"\n\n🔑 **2-Step Password**:\n`{session['two_step']}`"

    await message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "📩 Get OTP",
                callback_data=f"get_otp:{session['session_id']}"
            )],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
        ])
    )