from Nexa.core.client import app
import config

async def log_admin_action(text):
    try:
        await app.send_message(config.LOGS_CHANNEL, text)
    except Exception as e:
        print("Log error:", e)