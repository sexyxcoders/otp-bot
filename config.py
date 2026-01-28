import os

# ==============================
# Telegram API credentials
# ==============================
API_ID = int(os.getenv("API_ID", "22657083"))
API_HASH = os.getenv("API_HASH", "d6186691704bd901bdab275ceaab88f3")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7883129570:AAENeLvTsdrAmFxFgzW0yYSP2RMsQ4TElp4")

# ==============================
# Bot Details
# ==============================
BOT_NAME = os.getenv("BOT_NAME", "Neca")
BOT_USERNAME = os.getenv("BOT_USERNAME", "LucusMusicBot")

# ==============================
# Must Join Channel (without @)
# ==============================
# Must join channel (without @)
MUST_JOIN = "NexaCoders"

# ==============================
# Admin Telegram User IDs
# ==============================
ADMINS = [8422195674, 8553815122]  # apna Telegram user_id daalo

LOGS_CHANNEL = int(os.getenv("LOGS_CHANNEL", "-1003788903501"))

LOGS_CHANNEL = "@logchannelofsms"

# ==============================
# MongoDB Configuration 
# ==============================
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://krishvip39_db_user:Nqg0y3VXnfvacKRv@cluster0.e4cxyeg.mongodb.net/?appName=Cluster0")
DATABASE_NAME = os.getenv("DATABASE_NAME", "Ivan")

UPI_ID = "yourupi@upi"
UPI_NAME = "Nexa Store"
USDT_ADDRESS = "TRC20_WALLET_ADDRESS"

REFERRAL_PERCENT = 5   # 5% referral bonus

# ==============================
# Referral Settings
# ==============================
REFERRAL_BONUS = float(os.getenv("REFERRAL_BONUS", 5))

# ==============================
# Deposit Settings
# ==============================
MIN_DEPOSIT = float(os.getenv("MIN_DEPOSIT", 50))
UPI_ID = os.getenv("UPI_ID", "yourupi@upi")

# ==============================
# UPI QR Image Path
# ==============================
UPI_QR_IMAGE = os.getenv("UPI_QR_IMAGE", "Nexa/static/upi_qr.png")

# For rejection state
REJECT_STATE = {}

# ==============================
# Logging
# ==============================
LOG_FILE = os.getenv("LOG_FILE", "logs/nexa.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
