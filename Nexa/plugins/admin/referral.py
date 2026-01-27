from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from Nexa.database.mongo import referrals

@app.on_callback_query(filters.regex("^admin_referral$"))
async def admin_referral(client, callback):
    if callback.from_user.id not in config.ADMINS:
        return await callback.answer("❌ Not allowed", show_alert=True)

    total = referrals.count_documents({})
    percent = getattr(config, "REFERRAL_PERCENT", 5)
    text = f"🎁 Referral Stats:\n\nTotal Referrals: `{total}`\nReferral Bonus: `{percent}%`"

    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]]))