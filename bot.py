# bot.py
from Nexa.core.client import app

# Import all plugins so Pyrogram registers handlers
import Nexa.plugins           # user-facing plugins
import Nexa.plugins.admin     # admin plugins

if __name__ == "__main__":
    print("🚀 Bot is starting...")
    app.run()