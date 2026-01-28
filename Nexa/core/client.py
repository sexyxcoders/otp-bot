# Nexa/core/client.py
from pyrogram import Client
import config

app = Client(
    "NexaBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(
        root="Nexa/plugins"  # auto-load all plugins inside this folder
    )
)

print(">>> CLIENT INITIALIZED <<<")