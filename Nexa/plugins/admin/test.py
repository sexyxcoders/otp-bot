from Nexa.core.client import app
from pyrogram import filters

@app.on_message(filters.private)
async def test_cmd(_, msg):
    await msg.reply_text("✅ BOT IS RECEIVING MESSAGES")