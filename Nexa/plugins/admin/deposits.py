from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from Nexa.database.mongo import deposits
from Nexa.database.deposits import approve_deposit, update_deposit_status
from datetime import datetime, timedelta

EXPIRE_MINUTES = 10

# 🔄 Expire deposits older than EXPIRE_MINUTES
def expire_pending_deposits():
    expire_time = datetime.utcnow() - timedelta(minutes=EXPIRE_MINUTES)
    deposits.update_many(
        {"status": "pending", "created_at": {"$lt": expire_time}},
        {"$set": {"status": "expired"}}
    )


# 🔹 Show pending deposits or user deposits
@app.on_callback_query(filters.regex("^admin_deposits$"))
async def admin_deposits_cb(client, callback):
    if callback.from_user.id not in config.ADMINS:
        return await callback.answer("❌ Not allowed", show_alert=True)

    expire_pending_deposits()

    pending = list(deposits.find({"status": "pending"}).sort("created_at", -1).limit(20))

    if not pending:
        return await callback.message.edit_text(
            "📌 No pending deposits.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
        )

    text = "📌 **Pending Deposits**\n\n"
    buttons = []

    for d in pending:
        text += f"ID: `{d['id']}` | User: `{d['user_id']}` | ₹{d['amount']} | UTR: `{d.get('txid', 'N/A')}`\n"
        buttons.append([
            InlineKeyboardButton("✅ Approve", callback_data=f"admin_deposit_approve|{d['id']}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"admin_deposit_reject|{d['id']}"),
            InlineKeyboardButton("👀 By User", callback_data=f"admin_deposit_user|{d['user_id']}")
        ])

    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="admin_panel")])

    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))


# 🔹 Filter deposits by user
@app.on_callback_query(filters.regex(r"^admin_deposit_user\|(\d+)$"))
async def admin_deposit_by_user(client, callback):
    if callback.from_user.id not in config.ADMINS:
        return await callback.answer("❌ Not allowed", show_alert=True)

    user_id = int(callback.data.split("|")[1])
    user_deposits = list(deposits.find({"user_id": user_id}).sort("created_at", -1).limit(20))

    if not user_deposits:
        return await callback.answer(f"❌ No deposits found for user {user_id}", show_alert=True)

    text = f"📌 **Deposits for User {user_id}**\n\n"
    buttons = []

    for d in user_deposits:
        status_emoji = "✅" if d.get("status") == "approved" else "❌" if d.get("status") == "rejected" else "⏳"
        text += f"{status_emoji} ID: `{d['id']}` | ₹{d['amount']} | UTR: `{d.get('txid', 'N/A')}`\n"
        buttons.append([
            InlineKeyboardButton("✅ Approve", callback_data=f"admin_deposit_approve|{d['id']}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"admin_deposit_reject|{d['id']}")
        ])

    buttons.append([InlineKeyboardButton("🔙 Back to All Deposits", callback_data="admin_deposits")])
    buttons.append([InlineKeyboardButton("🏠 Admin Panel", callback_data="admin_panel")])

    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))


# 🔹 Approve / Reject deposit
@app.on_callback_query(filters.regex(r"^admin_deposit_(approve|reject)\|(\d+)$"))
async def admin_deposit_action(client, callback):
    if callback.from_user.id not in config.ADMINS:
        return await callback.answer("❌ Not allowed", show_alert=True)

    action, deposit_id = callback.data.split("|")
    deposit_id = int(deposit_id)

    dep = deposits.find_one({"id": deposit_id})
    if not dep:
        return await callback.answer("❌ Deposit not found", show_alert=True)
    if dep.get("status") != "pending":
        return await callback.answer("⚠️ Already processed", show_alert=True)

    if action == "admin_deposit_approve":
        approve_deposit(deposit_id)
        status_text = "✅ Approved"
    else:
        update_deposit_status(deposit_id, "rejected")
        status_text = "❌ Rejected"

    await callback.answer(status_text, show_alert=True)

    await callback.message.edit_text(
        f"💳 Deposit ID `{deposit_id}` processed: {status_text}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Deposits", callback_data="admin_deposits")],
            [InlineKeyboardButton("🏠 Admin Panel", callback_data="admin_panel")]
        ])
    )