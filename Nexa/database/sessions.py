from database.mongo import mongo
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class SessionManager:
    @staticmethod
    async def add_session(session_string: str, country: str, stock: int, price: float):
        """Add new session"""
        doc = {
            "session_string": session_string,
            "country": country,
            "stock": stock,
            "price": price,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=24)
        }
        await mongo.db.sessions.insert_one(doc)
    
    @staticmethod
    async def get_stock_by_country():
        """Get stock summary by country"""
        pipeline = [
            {"$match": {"stock": {"$gt": 0}}},
            {"$group": {
                "_id": "$country",
                "total_stock": {"$sum": "$stock"},
                "sessions": {"$sum": 1},
                "avg_price": {"$avg": "$price"}
            }},
            {"$sort": {"_id": 1}}
        ]
        return await mongo.db.sessions.aggregate(pipeline).to_list(None)
    
    @staticmethod
    async def get_all_sessions():
        """Get all sessions"""
        return await mongo.db.sessions.find({"stock": {"$gt": 0}}).to_list(None)
    
    @staticmethod
    async def remove_session(session_id: str):
        """Remove session"""
        await mongo.db.sessions.delete_one({"_id": session_id})

session_manager = SessionManager()