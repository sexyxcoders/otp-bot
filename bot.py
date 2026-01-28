# bot.py
from Nexa.core.client import app

# Import all plugins manually
import Nexa.plugins        # regular user plugins
import Nexa.Admin          # admin plugins

if __name__ == "__main__":
    print("🚀 Bot is starting...")
    app.run()