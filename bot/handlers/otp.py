from pyrogram import filters
from database.mongo import orders

def setup(app):

    @app.on_message(filters.command("myotp"))
    async def myotp(_, m):
        uid = m.from_user.id

        order = orders.find_one(
            {"user_id": uid},
            sort=[("_id", -1)]
        )

        if not order:
            return await m.reply("❌ No active order")

        if order["status"] == "waiting":
            return await m.reply("⏳ OTP not received yet")

        if order["status"] == "expired":
            return await m.reply("⌛ OTP expired & balance refunded")

        await m.reply(f"✅ **OTP:** `{order['otp']}`")