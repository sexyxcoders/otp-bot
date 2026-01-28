import os

# ----------------------------
# Bot / API
# ----------------------------
API_ID = int(os.getenv("API_ID", "123456"))        # Telegram API ID
API_HASH = os.getenv("API_HASH", "your_api_hash") # Telegram API Hash
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

# ----------------------------
# MongoDB
# ----------------------------
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

# ----------------------------
# Admins
# ----------------------------
ADMINS = [int(x) for x in os.getenv("ADMINS", "").split()]  # space-separated IDs

# ----------------------------
# Referral
# ----------------------------
REFERRAL_PERCENT = int(os.getenv("REFERRAL_PERCENT", "5"))