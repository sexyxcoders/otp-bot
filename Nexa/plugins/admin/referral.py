from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

from Nexa.database.users import is_admin
from Nexa.database.mongo import referrals

# admin temp state
REFRESH_REFERRAL_STATE = {}


# ================= MAIN REFERRAL PANEL =================
@app.on_callback_query(filters.regex("^admin_referral$"))
async def admin_referral_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    total = referrals.count_documents({})
    percent = getattr(config, "REFERRAL_PERCENT", 5)

    text = (
        "🎁 **Referral Management**\n\n"
        f"👥 Total Referrals: `{total}`\n"
        f"💰 Referral Bonus: `{percent}%`\n\n"
        "Choose an option below 👇"
    )

    await cq.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔄 Refresh User Referral", callback_data="admin_referral_refresh"),
                InlineKeyboardButton("📊 Referral Stats", callback_data="admin_referral_stats")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="admin_panel")
            ]
        ])
    )


# ================= REFERRAL STATS =================
@app.on_callback_query(filters.regex("^admin_referral_stats$"))
async def admin_referral_stats(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    total = referrals.count_documents({})
    unique_users = len(referrals.distinct("user_id"))

    await cq.message.edit_text(
        f"📊 **Referral Stats**\n\n"
        f"Total Entries: `{total}`\n"
        f"Unique Users: `{unique_users}`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="admin_referral")]
        ])
    )


# ================= REFRESH USER REFERRAL =================
@app.on_callback_query(filters.regex("^admin_referral_refresh$"))
async def admin_referral_refresh(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    REFRESH_REFERRAL_STATE[cq.from_user.id] = True

    await cq.message.edit_text(
        "🔄 **Refresh User Referral**\n\n"
        "Send the **USER ID** to refresh referral data.\n\n"
        "Example:\n`123456789`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="admin_referral")]
        ])
    )


# ================= INPUT HANDLER =================
@app.on_message(filters.private)
async def referral_input_handler(_, msg):
    if msg.from_user.id not in REFRESH_REFERRAL_STATE:
        return

    if not is_admin(msg.from_user.id):
        REFRESH_REFERRAL_STATE.pop(msg.from_user.id, None)
        return

    REFRESH_REFERRAL_STATE.pop(msg.from_user.id, None)

    try:
        user_id = int(msg.text.strip())
    except ValueError:
        return await msg.reply("❌ Invalid USER ID.")

    result = referrals.delete_many({"user_id": user_id})

    await msg.reply(
        f"✅ **Referral Refreshed**\n\n"
        f"👤 User ID: `{user_id}`\n"
        f"🗑 Removed Records: `{result.deleted_count}`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎁 Referral Panel", callback_data="admin_referral")]
        ])
    )