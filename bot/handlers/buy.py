import time
from pyrogram import filters
from database.users import get_user, deduct
from database.numbers import get_free, mark_used
from database.orders import create_order
from config import PRICE

def setup(app):

    @app.on_callback_query(filters.regex("^buy_"))
    async def buy(_, q):
        uid = q.from_user.id
        country = q.data.split("_")[1]

        user = get_user(uid)
        if not user or user["balance"] < PRICE:
            return await q.message.edit("❌ Insufficient balance")

        num = get_free(country)
        if not num:
            return await q.message.edit("❌ No number available")

        deduct(uid, PRICE)
        mark_used(num["_id"])

        create_order(uid, num["phone"], num["session"])

        await q.message.edit(
            f"📞 **Number Allocated**\n\n"
            f"`{num['phone']}`\n\n"
            f"💰 Price: ₹{PRICE}\n"
            f"⏳ OTP valid for 10 minutes\n\n"
            f"Use /myotp to check OTP"
        )