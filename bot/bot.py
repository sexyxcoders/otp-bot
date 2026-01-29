from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

from bot.handlers import start, buy, otp, deposit

app = Client(
    "otp-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

start.setup(app)
buy.setup(app)
otp.setup(app)
deposit.setup(app)

print("🤖 OTP Bot Started")
app.run()