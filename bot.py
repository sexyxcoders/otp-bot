# bot.py
from Nexa.core.client import app

# Import plugins after app is ready
import Nexa.plugins

if __name__ == "__main__":
    print("🚀 Bot is starting...")
    app.run()