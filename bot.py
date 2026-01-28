# bot.py
from Nexa.core.client import app

# Import plugins AFTER app is initialized
import Nexa.plugins         # root plugins

import Nexa.plugins.admin   # admin plugins

if __name__ == "__main__":
    print("🚀 Bot is starting...")
    app.run()