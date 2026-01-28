from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import asyncio
import config
from Nexa.database.mongo import users

BROADCAST_STATE = {}

@app.on_callback_query(filters.regex("^admin_broadcast$"))
async def admin_broadcast_cb(client, cq):
    if cq.from_user.id not in config.ADMINS:
        return await cq.answer("❌ Not allowed", show_alert=True)

    BROADCAST_STATE[cq.from_user.id] = True
    await cq.message.edit_text(
        "📣 **Broadcast Mode**\n\n"
        "Send the message (text, photo, video, document, etc.) to broadcast to all users.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="admin_broadcast_cancel")]
        ])
    )

@app.on_callback_query(filters.regex("^admin_broadcast_cancel$"))
async def admin_broadcast_cancel_cb(client, cq):
    BROADCAST_STATE.pop(cq.from_user.id, None)
    await cq.message.edit_text(
        "❌ **Broadcast Cancelled**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
        ])
    )

@app.on_message(filters.private & filters.user(config.ADMINS))
async def broadcast_handler(client, msg: Message):
    if not BROADCAST_STATE.get(msg.from_user.id):
        return msg.continue_propagation()

    BROADCAST_STATE.pop(msg.from_user.id)
    status_msg = await msg.reply_text("📣 **Broadcast started...**")

    all_users = list(users.find({}, {"user_id": 1}))
    sent = 0
    failed = 0

    for u in all_users:
        try:
            await msg.copy(chat_id=u["user_id"])
            sent += 1
            await asyncio.sleep(0.05)
        except Exception:
            failed += 1
            continue

    await status_msg.edit_text(
        f"📣 **Broadcast Completed**\n\n"
        f"✅ Sent: `{sent}`\n"
        f"❌ Failed: `{failed}`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
        ])
    )