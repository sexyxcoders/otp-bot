from Nexa.core.client import app

@app.on_message()
async def test_handler(client, msg):
    await msg.reply_text("✅ BOT IS ALIVE")