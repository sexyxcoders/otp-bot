from pyrogram import Client, enums
import config

app = Client(
    name="NexaBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    workers=10,
    in_memory=True,
    parse_mode=enums.ParseMode.MARKDOWN,
    plugins=dict(root="Nexa.plugins")
)