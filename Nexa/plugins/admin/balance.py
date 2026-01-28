from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.core.client import app
from Nexa.database.users import get_balance, add_balance, deduct_balance, is_admin

# Track admin state for balance operations
BALANCE_STATE = {}

# -----------------------
# Admin: Add Balance Button
# -----------------------
@app.on_callback_query(filters.regex("^admin_add_balance$"))
async def admin_add_balance_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    BALANCE_STATE[cq.from_user.id] = "add"
    await cq.message.edit_text(
        "➕ **Add Balance**\n\n"
        "Send the message in this format:\n"
        "`<user_id> <amount>`\n\n"
        "Example: `123456789 50`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="admin_balance_cancel")]
        ])
    )
    await cq.answer()

# -----------------------
# Admin: Subtract Balance Button
# -----------------------
@app.on_callback_query(filters.regex("^admin_sub_balance$"))
async def admin_sub_balance_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    BALANCE_STATE[cq.from_user.id] = "sub"
    await cq.message.edit_text(
        "➖ **Subtract Balance**\n\n"
        "Send the message in this format:\n"
        "`<user_id> <amount>`\n\n"
        "Example: `123456789 50`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="admin_balance_cancel")]
        ])
    )
    await cq.answer()

# -----------------------
# Admin: Cancel Operation
# -----------------------
@app.on_callback_query(filters.regex("^admin_balance_cancel$"))
async def admin_balance_cancel(_, cq):
    BALANCE_STATE.pop(cq.from_user.id, None)
    await cq.message.edit_text(
        "❌ **Operation Cancelled**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Back to Admin Panel", callback_data="admin_panel")]
        ])
    )
    await cq.answer()

# -----------------------
# Admin: Handle Input Message
# -----------------------
@app.on_message(filters.private)
async def handle_balance_input(_, message):
    admin_id = message.from_user.id
    if admin_id not in BALANCE_STATE:
        return  # Not in balance operation

    try:
        user_id_str, amount_str = message.text.split()
        user_id = int(user_id_str)
        amount = float(amount_str)
    except Exception:
        return await message.reply("❌ Invalid format. Use `<user_id> <amount>`")

    operation = BALANCE_STATE[admin_id]
    if operation == "add":
        add_balance(user_id, amount)
        text = f"✅ Added ₹{amount} to user `{user_id}`.\nNew Balance: ₹{get_balance(user_id)}"
    else:
        deduct_balance(user_id, amount)
        text = f"✅ Subtracted ₹{amount} from user `{user_id}`.\nNew Balance: ₹{get_balance(user_id)}"

    BALANCE_STATE.pop(admin_id, None)

    await message.reply(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Back to Admin Panel", callback_data="admin_panel")]
        ])
    )