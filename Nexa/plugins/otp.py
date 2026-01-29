from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from core.client import app
from core.otp_manager import otp_manager
from database.users import user_manager, mongo

@app.on_callback_query(filters.regex("^get_otp$"))
async def get_otp(client, callback: CallbackQuery):
    user_id = callback.from_user.id
    user = await mongo.db.users.find_one({"user_id": user_id})
    
    if not user or user["balance"] <= 0:
        await callback.answer("❌ No balance! Contact admin.", show_alert=True)
        return
    
    await callback.message.edit_text("🔄 **Assigning session...**")
    
    session = await otp_manager.assign_session(user_id)
    if session:
        await callback.message.edit_text(
            f"✅ **Session Assigned!**\n\n"
            f"📱 **Number:** `{session}`\n"
            f"⏳ **Polling OTP** (10-60s)...\n"
            f"💰 **Balance:** `${user['balance']:.2f}`",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⏳ Status", callback_data="otp_status")]
            ]),
            parse_mode="Markdown"
        )
    else:
        await callback.message.edit_text(
            "❌ **No sessions available**\nTry again later.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Retry", callback_data="get_otp")]
            ])
        )

@app.on_callback_query(filters.regex("^otp_status$"))
async def otp_status(client, callback: CallbackQuery):
    await callback.answer("⏳ Still polling for OTP...", show_alert=True)