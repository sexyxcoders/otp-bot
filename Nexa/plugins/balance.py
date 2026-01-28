# Nexa/plugins/balance.py

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.core.client import app
from Nexa.database.users import get_balance, add_balance, deduct_balance, ensure_user

# ----------------------------
# Check balance
# ----------------------------
@app.on_message(filters.private & filters.command("balance"))
async def balance_cmd(_, msg):
    ensure_user(msg.from_user.id)  # make sure user exists in DB
    bal = get_balance(msg.from_user.id)
    await msg.reply_text(
        f"💰 Your current balance is: ₹{bal}",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("➕ Add Balance", callback_data=f"user_add_balance"),
                InlineKeyboardButton("➖ Subtract Balance", callback_data=f"user_sub_balance")
            ]
        ])
    )

# ----------------------------
# Add balance (via inline button)
# ----------------------------
@app.on_callback_query(filters.regex("^user_add_balance$"))
async def add_balance_cb(_, cq):
    ensure_user(cq.from_user.id)
    amount = 10  # default example amount
    add_balance(cq.from_user.id, amount)
    bal = get_balance(cq.from_user.id)
    await cq.answer(f"✅ ₹{amount} added! New Balance: ₹{bal}", show_alert=True)

# ----------------------------
# Subtract balance (via inline button)
# ----------------------------
@app.on_callback_query(filters.regex("^user_sub_balance$"))
async def sub_balance_cb(_, cq):
    ensure_user(cq.from_user.id)
    amount = 5  # default example amount
    deduct_balance(cq.from_user.id, amount)
    bal = get_balance(cq.from_user.id)
    await cq.answer(f"✅ ₹{amount} subtracted! New Balance: ₹{bal}", show_alert=True)