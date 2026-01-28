from pyrogram import filters
from Nexa.core.client import app
from Nexa.database.users import get_balance, deduct_balance
from Nexa.database.sessions import assign_session_to_user


@app.on_callback_query(filters.regex("^confirm_buy:"))
async def buy_confirm_cb(client, cq):
    await cq.answer()

    user_id = cq.from_user.id
    country = cq.data.split(":")[1]

    session = assign_session_to_user(user_id, country)
    if not session:
        return await cq.message.reply("❌ Out of stock.")

    price = session["price"]
    if get_balance(user_id) < price:
        return await cq.message.reply("❌ Insufficient balance.")

    deduct_balance(user_id, price)

    await cq.message.edit_text(
        "✅ **Purchase Successful**\n\n"
        "Preparing your number...",
        reply_markup=None
    )

    from Nexa.plugins.sessions.delivery import deliver_session
    await deliver_session(client, cq.message, session)