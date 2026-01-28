import os

# ----------------------------
# Bot / API
# ----------------------------
API_ID = int(os.getenv("API_ID", "22657083"))        # Telegram API ID
API_HASH = os.getenv("API_HASH", "d6186691704bd901bdab275ceaab88f3") # Telegram API Hash
BOT_TOKEN = os.getenv("BOT_TOKEN", "7883129570:AAENeLvTsdrAmFxFgzW0yYSP2RMsQ4TElp4")

# ----------------------------
# MongoDB
# ----------------------------
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://krishvip39_db_user:Nqg0y3VXnfvacKRv@cluster0.e4cxyeg.mongodb.net/?appName=Cluster0")

# ----------------------------
# Admins
# ----------------------------
ADMINS = [int(x) for x in os.getenv("ADMINS", "8553815122").split()]  # space-separated IDs

