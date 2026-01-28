from Nexa.core.client import app
from pyrogram import filters

print(">>> TEST ROOT PLUGIN LOADED <<<")

@app.on_message()
async def debug_receive(client, msg):
    print(">>> MESSAGE RECEIVED:", msg.text, msg.from_user.id)
    await msg.reply_text(f"✅ RECEIVED: {msg.text}")