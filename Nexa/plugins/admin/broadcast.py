from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import FloodWait
import config
from Nexa.database.mongo import users
import asyncio

# ---------------------------
# BROADCAST STATE
# Keeps track of admins in broadcast mode and cancel flag
# ---------------------------
BROADCAST_STATE = {}  # {admin_id: {"active": True, "cancel": False}}

# ---------------------------
# OPEN BROADCAST MODE
# ---------------------------
@app.on_callback_query(filters.regex("^admin_broadcast$"))
async def admin_broadcast_cb(client, cq):
    if cq.from_user.id not in config.ADMINS:
        return await cq.answer("❌ Not allowed", show_alert=True)

    # Activate broadcast mode
    BROADCAST_STATE[cq.from_user.id] = {"active": True, "cancel": False}

    await cq.message.edit_text(
        "📣 **Broadcast Mode Activated**\n\n"
        "Send any message (text, photo, video, document, etc.) to broadcast to all users.\n\n"
        "Press ❌ Cancel to exit broadcast mode.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="admin_broadcast_cancel")]
        ])
    )

# ---------------------------
# CANCEL BROADCAST MODE
# ---------------------------
@app.on_callback_query(filters.regex("^admin_broadcast_cancel$"))
async def admin_broadcast_cancel_cb(client, cq):
    state = BROADCAST_STATE.get(cq.from_user.id)
    if state:
        state["cancel"] = True
        await cq.answer("❌ Broadcast cancelled!", show_alert=True)
        await cq.message.edit_text(
            "❌ **Broadcast Cancelled**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
            ])
        )
    else:
        await cq.answer("No broadcast in progress", show_alert=True)

# ---------------------------
# HANDLE BROADCAST MESSAGE
# ---------------------------
@app.on_message(filters.user(config.ADMINS))
async def broadcast_handler(client, msg: Message):
    state = BROADCAST_STATE.get(msg.from_user.id)
    if not state or state.get("cancel") or not state.get("active"):
        return  # Admin not in broadcast mode

    # Mark active False to prevent multiple triggers
    state["active"] = False

    await start_broadcast(msg, state)

# ---------------------------
# BROADCAST LOGIC
# ---------------------------
async def start_broadcast(msg: Message, state):
    status_msg = await msg.reply_text("📣 **Broadcast started...**")

    all_users = list(users.find({}, {"user_id": 1}))
    total = len(all_users)
    sent = 0
    failed = 0

    for i, u in enumerate(all_users, start=1):
        # Stop if admin cancels mid-way
        if state.get("cancel"):
            await status_msg.edit_text(
                f"❌ **Broadcast Cancelled Midway**\n\n"
                f"✅ Sent: `{sent}`\n"
                f"❌ Failed: `{failed}`\n"
                f"📊 Progress: {i-1}/{total}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
                ])
            )
            BROADCAST_STATE.pop(msg.from_user.id, None)
            return

        try:
            await msg.copy(chat_id=u["user_id"])
            sent += 1

            # Update progress every 50 users
            if i % 50 == 0:
                await status_msg.edit_text(
                    f"📣 **Broadcast in progress...**\n\n"
                    f"✅ Sent: {sent}\n"
                    f"❌ Failed: {failed}\n"
                    f"📊 Progress: {i}/{total}"
                )

            await asyncio.sleep(0.3)  # avoid flood
        except FloodWait as e:
            await asyncio.sleep(e.value)
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

    # Clean up
    BROADCAST_STATE.pop(msg.from_user.id, None)