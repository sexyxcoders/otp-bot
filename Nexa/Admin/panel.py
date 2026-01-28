from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

@app.on_callback_query(filters.regex("^admin_panel$"))
async def admin_panel_cb(client, cq):
    if cq.from_user.id not in config.ADMINS:
        return await cq.answer("❌ Not allowed", show_alert=True)

    buttons = [
        [InlineKeyboardButton("📣 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("👥 Users", callback_data="admin_users")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]

    await cq.message.edit_text(
        "👑 **Admin Panel**\n\nSelect an option below:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )