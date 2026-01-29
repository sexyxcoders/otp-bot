import time
from database.mongo import orders
from database.numbers import free_number
from database.users import add_balance
from config import OTP_EXPIRY, PRICE

print("⏱ Expiry worker started")

while True:
    now = int(time.time())

    # find all waiting orders
    for o in orders.find({"status": "waiting"}):
        if now - o["created_at"] > OTP_EXPIRY:
            # expire order
            orders.update_one(
                {"_id": o["_id"]},
                {"$set": {"status": "expired"}}
            )

            # free the number
            free_number(o["phone"])

            # refund user balance
            add_balance(o["user_id"], PRICE)

            print(f"⌛ Expired order {o['_id']} - refunded ₹{PRICE}")

    time.sleep(30)