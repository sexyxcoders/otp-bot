from pyrogram import Client
import config  # import your config.py

app = Client(
    "NexaBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(
        root=[]  # Plugins are manually imported in bot.py
    )
)

print(">>> CLIENT INITIALIZED <<<")