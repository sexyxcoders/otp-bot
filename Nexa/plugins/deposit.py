from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

import config

# Correct imports for your folder structure
from Nexa.database.mongo import db, users, deposits, referrals
from Nexa.database.deposits import (
    add_deposit,
    get_deposit_by_id,
    approve_deposit,
    update_deposit_status
)

USER_STATE = {}
USER_DATA = {}

EXPIRY_TIME = 10 * 60
SCANNER_IMAGE = "https://graph.org/file/6216107c5a50d5acf1f3d-e7a5918c1578ddfd3a.jpg"


def expire_deposits():
    expire_after = int(time.time()) - EXPIRY_TIME
    deposits.update_many(
        {"status": "pending", "created_at": {"$lt": expire_after}},
        {"$set": {"status": "expired"}}
    )


@app.on_callback_query(filters.regex("^deposit$"))
async def deposit_btn(client, callback):
    user_id = callback.from_user.id

    USER_STATE[user_id] = "AMOUNT"
    users.update_one(
        {"user_id": user_id},
        {"$setOnInsert": {"balance": 0}},
        upsert=True
    )

    text = (
        "💰 **Deposit Started**\n\n"
        f"🏦 **UPI ID:** `{config.UPI_ID}`\n"
        f"👤 **Name:** `{config.UPI_NAME}`\n\n"
        "📌 Step 1: Send amount\n"
        "Example: `500`"
    )

    await callback.message.reply_photo(
        photo=SCANNER_IMAGE,
        caption=text
    )
    await callback.answer()


@app.on_message(filters.private & filters.text)
async def deposit_text(client, message):
    user_id = message.from_user.id

    if user_id not in USER_STATE:
        return

    # Expire old deposits
    expire_deposits()

    if USER_STATE[user_id] == "AMOUNT":
        if not message.text.isdigit():
            return await message.reply("❌ Enter valid amount")

        USER_DATA[user_id] = {
            "amount": int(message.text),
            "start": time.time()
        }
        USER_STATE[user_id] = "UTR"
        return await message.reply("📌 Step 2: Send UTR / TXID")

    if USER_STATE[user_id] == "UTR":
        utr = message.text.strip()

        # Duplicate UTR check
        if deposits.find_one({"txid": utr}):
            return await message.reply("❌ Duplicate UTR detected!")

        USER_DATA[user_id]["txid"] = utr
        USER_STATE[user_id] = "SCREENSHOT"
        return await message.reply("📸 Step 3: Send screenshot")


@app.on_message(filters.private & filters.photo)
async def deposit_photo(client, message):
    user_id = message.from_user.id

    if USER_STATE.get(user_id) != "SCREENSHOT":
        return

    data = USER_DATA[user_id]

    if time.time() - data["start"] > EXPIRY_TIME:
        USER_STATE.pop(user_id)
        USER_DATA.pop(user_id)
        return await message.reply("⏱ Deposit expired. Start again.")

    # Save deposit in DB
    deposit = add_deposit(
        user_id=user_id,
        amount=data["amount"],
        txid=data["txid"],
        proof=message.photo.file_id
    )

    caption = (
        "💰 **New Deposit Request**\n\n"
        f"👤 {message.from_user.mention}\n"
        f"🆔 `{user_id}`\n"
        f"💵 `{data['amount']}`\n"
        f"📄 `{data['txid']}`\n"
        f"🧾 Deposit ID: `{deposit['id']}`"
    )

    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("✅ Approve", callback_data=f"approve|{deposit['id']}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject|{deposit['id']}")
        ]]
    )

    await client.send_photo(
        chat_id=config.LOGS_CHANNEL,
        photo=message.photo.file_id,
        caption=caption,
        reply_markup=buttons
    )

    await message.reply("✅ Deposit sent for admin approval ⏳")

    USER_STATE.pop(user_id)
    USER_DATA.pop(user_id)


@app.on_callback_query(filters.regex("^(approve|reject)\|"))
async def admin_action(client, callback):
    if callback.from_user.id not in config.ADMINS:
        return await callback.answer("Not allowed", True)

    action, dep_id = callback.data.split("|")
    dep_id = int(dep_id)

    deposit = get_deposit_by_id(dep_id)
    if not deposit or deposit["status"] != "pending":
        return await callback.answer("Already processed", True)

    user_id = deposit["user_id"]
    amount = deposit["amount"]

    if action == "approve":
        approve_deposit(dep_id)

        await client.send_message(
            user_id,
            f"✅ Deposit approved!\n💵 Amount credited: `{amount}`\n"
            f"💰 New Balance: `{users.find_one({'user_id': user_id})['balance']}`"
        )

        await callback.message.edit_caption(
            callback.message.caption + "\n\n✅ APPROVED"
        )

    else:
        update_deposit_status(dep_id, "rejected")
        await client.send_message(user_id, "❌ Deposit rejected. Contact support.")
        await callback.message.edit_caption(
            callback.message.caption + "\n\n❌ REJECTED"
        )

    await callback.answer("Done ✅")