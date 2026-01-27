from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from Nexa.database.mongo import users
import asyncio

BROADCAST_STATE = {}

@app.on_callback_query(filters.regex("^admin_broadcast$"))
async def admin_broadcast(client, callback):
    if callback.from_user.id not in config.ADMINS:
        return await callback.answer("❌ Not allowed", show_alert=True)

    BROADCAST_STATE[callback.from_user.id] = True
    await callback.message.edit_text(
        "📣 **Broadcast**\n\n"
        "Send the message (text, photo, video, etc.) you want to broadcast to all users.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="admin_broadcast_cancel")]])
    )


@app.on_callback_query(filters.regex("^admin_broadcast_cancel$"))
async def admin_broadcast_cancel(client, callback):
    BROADCAST_STATE.pop(callback.from_user.id, None)
    await callback.message.edit_text(
        "❌ **Broadcast Cancelled**",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )


@app.on_message(filters.private & filters.user(config.ADMINS))
async def broadcast_handler(client, message):
    if not BROADCAST_STATE.get(message.from_user.id):
        return message.continue_propagation()

    BROADCAST_STATE.pop(message.from_user.id)

    status_msg = await message.reply_text("📣 **Broadcasting started...**")

    all_users = list(users.find({}, {"user_id": 1}))
    sent = 0
    failed = 0

    for u in all_users:
        try:
            await message.copy(chat_id=u["user_id"])
            sent += 1
            await asyncio.sleep(0.1)
        except Exception:
            failed += 1
            continue

    await status_msg.edit_text(
        f"📣 **Broadcast Completed**\n\n"
        f"✅ Sent: `{sent}`\n"
        f"❌ Failed: `{failed}`",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )