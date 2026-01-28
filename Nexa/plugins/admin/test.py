from Nexa.core.client import app
from pyrogram import filters

@app.on_message(filters.private & filters.command("test"))
async def test_cmd(_, message):
    await message.reply_text("✅ TEST COMMAND WORKING")