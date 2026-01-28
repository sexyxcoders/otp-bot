from pyrogram import Client
import config

print(">>> CLIENT INITIALIZED <<<")

app = Client(
    name="nexa-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="Nexa.plugins")  # 🔥 THIS LINE FIXED
)