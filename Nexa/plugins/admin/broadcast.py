import asyncio
from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin, get_all_users

BROADCAST_STATE = {}

@app.on_callback_query(filters.regex("^admin_broadcast$"))
async def admin_broadcast_cb(client, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    BROADCAST_STATE[cq.from_user.id] = True
    await cq.message.edit_text(
        "📣 Send the message to broadcast to all users.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="admin_broadcast_cancel")]])
    )

@app.on_message(filters.private & filters.user(list(BROADCAST_STATE.keys())))
async def broadcast_handler(client, message):
    if not BROADCAST_STATE.get(message.from_user.id):
        return

    BROADCAST_STATE.pop(message.from_user.id)
    sent = failed = 0

    for u in get_all_users():
        try:
            await message.copy(chat_id=u["user_id"])
            sent += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1

    await message.reply(f"📣 Broadcast completed ✅\nSent: {sent}\nFailed: {failed}")