import re
from pyrogram import Client, filters
from pyrogram.session import StringSession
from database.mongo import orders
from database.orders import set_otp
from database.numbers import free_number
from config import API_ID, API_HASH

OTP_REGEX = r"\b\d{4,6}\b"  # matches 4-6 digit OTP

# Get all unique sessions
sessions = orders.distinct("session")

clients = []

for s in sessions:
    app = Client(
        StringSession(s),
        api_id=API_ID,
        api_hash=API_HASH
    )

    @app.on_message(filters.private)
    async def read_otp(_, m):
        if not m.text:
            return

        match = re.search(OTP_REGEX, m.text)
        if not match:
            return

        otp = match.group()

        # Find the latest waiting order for this session
        order = orders.find_one(
            {"session": s, "status": "waiting"},
            sort=[("_id", -1)]
        )

        if order:
            set_otp(order["_id"], otp)
            print(f"✅ OTP received: {otp} for order {order['_id']}")

    app.start()
    clients.append(app)

print("🚀 OTP Listener started for all sessions")

# Keep alive
import time
while True:
    time.sleep(10)