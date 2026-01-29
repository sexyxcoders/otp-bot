from pyrogram import filters
from database.users import add_balance, get_user
from config import ADMIN_ID

def setup(app):

    @app.on_message(filters.command("deposit") & filters.user(ADMIN_ID))
    async def deposit(_, m):
        try:
            _, uid, amount = m.text.split()
            uid = int(uid)
            amount = int(amount)
        except:
            return await m.reply("Usage:\n/deposit USER_ID AMOUNT")

        if not get_user(uid):
            return await m.reply("❌ User not found")

        add_balance(uid, amount)
        await m.reply(f"✅ Added ₹{amount} to `{uid}`")