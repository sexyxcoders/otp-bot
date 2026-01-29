from pyrogram import filters
from bot.keyboards import country_keyboard
from database.users import get_user, create_user

def setup(app):

    @app.on_message(filters.command("start"))
    async def start(_, m):
        uid = m.from_user.id

        if not get_user(uid):
            create_user(uid)

        await m.reply(
            "📲 **OTP SERVICE PANEL**\n\n"
            "Select country to buy number 👇",
            reply_markup=country_keyboard()
        )