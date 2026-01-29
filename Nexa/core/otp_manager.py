import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
from database.mongo import mongo
from database.users import user_manager
from database.sessions import session_manager
from core.client import app
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OTPManager:
    def __init__(self):
        self.active_polls: Dict[int, asyncio.Task] = {}
    
    async def assign_session(self, user_id: int) -> Optional[str]:
        """Assign session with available stock"""
        try:
            # Get available session
            session = await mongo.db.sessions.find_one_and_update(
                {"stock": {"$gt": 0}},
                {"$inc": {"stock": -1}},
                sort=[("stock", -1)]
            )
            
            if not session:
                return None
            
            session_number = session["session_string"]
            price = session["price"]
            
            # Update user session
            await mongo.db.users.update_one(
                {"user_id": user_id},
                {"$set": {
                    "active_session": {
                        "session_number": session_number,
                        "country": session["country"],
                        "price": price,
                        "assigned_at": datetime.utcnow()
                    }
                }}
            )
            
            # Start polling
            await self.start_polling(user_id, session_number)
            return session_number
            
        except Exception as e:
            logger.error(f"Assign session error: {e}")
            return None
    
    async def start_polling(self, user_id: int, session_number: str):
        """Start OTP polling"""
        if user_id in self.active_polls:
            self.active_polls[user_id].cancel()
        
        task = asyncio.create_task(self._poll_otp(user_id, session_number))
        self.active_polls[user_id] = task
    
    async def _poll_otp(self, user_id: int, session_number: str):
        """Poll SMS API for OTP"""
        max_attempts = 120  # 10 minutes
        
        for i in range(max_attempts):
            try:
                # 🚨 REPLACE WITH YOUR SMS API
                otp = await self._get_sms_from_provider(session_number)
                
                if otp:
                    await self._send_otp_to_user(user_id, session_number, otp)
                    break
                
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"Poll error: {e}")
                await asyncio.sleep(5)
        
        if user_id in self.active_polls:
            del self.active_polls[user_id]
    
    async def _get_sms_from_provider(self, session_number: str) -> Optional[str]:
        """🔧 IMPLEMENT YOUR SMS PROVIDER API HERE"""
        # Example SMS-Activate / SMSPVA API
        await asyncio.sleep(3)  # Simulate API delay
        
        # SIMULATED OTP - REMOVE IN PRODUCTION
        import random
        if random.random() > 0.7:
            return f"{random.randint(100000, 999999)}"
        
        return None
    
    async def _send_otp_to_user(self, user_id: int, session_number: str, otp: str):
        """Send OTP to user and deduct balance"""
        try:
            user = await mongo.db.users.find_one({"user_id": user_id})
            if not user:
                return
            
            session_doc = await mongo.db.sessions.find_one(
                {"session_string": session_number}
            )
            price = session_doc["price"] if session_doc else 0
            
            if user["balance"] >= price:
                # Deduct balance
                await mongo.db.users.update_one(
                    {"user_id": user_id},
                    {"$inc": {"balance": -price}}
                )
                
                # Store OTP
                await mongo.db.otp_codes.insert_one({
                    "user_id": user_id,
                    "session_number": session_number,
                    "otp": otp,
                    "delivered_at": datetime.utcnow(),
                    "expires_at": datetime.utcnow() + timedelta(minutes=10)
                })
                
                # Send to user
                await app.send_message(
                    user_id,
                    f"✅ **OTP RECEIVED!**\n\n"
                    f"📱 `{session_number}`\n"
                    f"🔢 **{otp}**\n"
                    f"💰 **-${price:.2f}** (Balance: ${user['balance'] - price:.2f})"
                )
            else:
                await app.send_message(user_id, f"❌ Insufficient balance! Need ${price:.2f}")
                
        except Exception as e:
            logger.error(f"Send OTP error: {e}")

otp_manager = OTPManager()