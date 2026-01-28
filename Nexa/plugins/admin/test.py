from Nexa.core.client import app

@app.on_message()
async def test_receive(client, msg):
    print("Received from:", msg.from_user.id)
    await msg.reply_text(f"Got your message: {msg.text or 'media'}")
