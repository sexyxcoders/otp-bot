from pymongo import MongoClient
import config

MONGO_URL = config.MONGO_URL  # add this in config.py

client = MongoClient(MONGO_URL)
db = client["nexa_db"]

users = db["users"]
orders = db["orders"]
deposits = db["deposits"]
referrals = db["referrals"]  # ADD THIS
sessions = db["sessions"]
countries = db["countries"]
otp_codes = db["otp_codes"]
counters = db["counters"]