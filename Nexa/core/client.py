from pyrogram import Client
import os
import config

app = Client(
    "NexaBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(
        root=[]  # Plugins are manually imported in bot.py
    )
)

print(">>> CLIENT INITIALIZED <<<")