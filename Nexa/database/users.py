from database.mongo import mongo
from datetime import datetime

class UserManager:
    @staticmethod
    async def ensure_user(user_id: int, username: str = ""):
        """Create or get user"""
        user = await mongo.db.users.find_one({"user_id": user_id})
        if not user:
            user = {
                "user_id": user_id,
                "username": username,
                "balance": 0.0,
                "total_otps": 0,
                "created_at": datetime.utcnow()
            }
            await mongo.db.users.insert_one(user)
        return user
    
    @staticmethod
    async def add_balance(user_id: int, amount: float):
        """Add balance to user"""
        await mongo.db.users.update_one(
            {"user_id": user_id},
            {"$inc": {"balance": amount}}
        )
    
    @staticmethod
    async def deduct_balance(user_id: int, amount: float) -> bool:
        """Deduct balance if sufficient"""
        result = await mongo.db.users.update_one(
            {"user_id": user_id, "balance": {"$gte": amount}},
            {"$inc": {"balance": -amount, "total_otps": 1}}
        )
        return result.modified_count > 0

user_manager = UserManager()