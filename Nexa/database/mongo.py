import motor.motor_asyncio
import os
from dotenv import load_dotenv
import config

load_dotenv()

class MongoDB:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
        self.db = self.client[os.getenv("DB_NAME", "nexa_otp")]
        
        # Auto-expire collections
        self.db.otp_codes.create_index("expires_at", expireAfterSeconds=0)

mongo = MongoDB()