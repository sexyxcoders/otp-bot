from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import config
from Nexa.database.mongo import users
import asyncio

# Track which admin is in broadcast mode
BROADCAST_STATE = {}

# ---------------------------
# OPEN BROADCAST MODE
# ---------------------------
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


# ---------------------------
# CANCEL BROADCAST MODE
# ---------------------------
@app.on_callback_query(filters.regex("^admin_broadcast_cancel$"))
async def admin_broadcast_cancel_cb(client, cq):
    BROADCAST_STATE.pop(cq.from_user.id, None)
    await cq.message.edit_text(
        "❌ **Broadcast Cancelled**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
        ])
    )


# ---------------------------
# HANDLE BROADCAST MESSAGE
# ---------------------------
@app.on_message(filters.private & filters.user(config.ADMINS))
async def broadcast_handler(client, msg: Message):
    if not BROADCAST_STATE.get(msg.from_user.id):
        return msg.continue_propagation()

    # Remove admin from broadcast state
    BROADCAST_STATE.pop(msg.from_user.id)

    # Notify admin
    status_msg = await msg.reply_text("📣 **Broadcast started...**")

    # Fetch all users
    all_users = list(users.find({}, {"user_id": 1}))
    sent = 0
    failed = 0

    for u in all_users:
        try:
            # Copy message to user
            await msg.copy(chat_id=u["user_id"])
            sent += 1
            # slight delay to prevent flood
            await asyncio.sleep(0.05)
        except Exception:
            failed += 1
            continue

    # Broadcast completed
    await status_msg.edit_text(
        f"📣 **Broadcast Completed**\n\n"
        f"✅ Sent: `{sent}`\n"
        f"❌ Failed: `{failed}`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
        ])
    ) 