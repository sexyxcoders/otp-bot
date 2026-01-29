from database.mongo import mongo

class OTPCodeManager:
    @staticmethod
    async def store_otp(session_number: str, otp: str, user_id: int):
        """Store received OTP"""
        await mongo.db.otp_codes.insert_one({
            "session_number": session_number,
            "otp": otp,
            "user_id": user_id,
            "received_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(minutes=10)
        })
    
    @staticmethod
    async def get_user_otps(user_id: int, limit: int = 10):
        """Get user's recent OTPs"""
        return await mongo.db.otp_codes.find(
            {"user_id": user_id}
        ).sort("received_at", -1).limit(limit).to_list(None)

otp_codes_manager = OTPCodeManager()