from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from core.client import app
from database.sessions import mongo
import os
from dotenv import load_dotenv

load_dotenv()
ADMIN_ID = int(os.getenv("ADMIN_ID"))

@app.on_callback_query(filters.regex("^admin_stock$") & filters.user(ADMIN_ID))
async def admin_stock(client, callback: CallbackQuery):
    stock = await mongo.db.sessions.aggregate([
        {"$match": {"stock": {"$gt": 0}}},
        {"$group": {
            "_id": "$country",
            "total_stock": {"$sum": "$stock"},
            "sessions": {"$sum": 1}
        }}
    ]).to_list(None)
    
    text = "📊 **STOCK BY COUNTRY:**\n\n"
    total = 0
    for item in stock:
        text += f"🌍 **{item['_id']}**: {item['total_stock']} sessions\n"
        total += item['total_stock']
    
    text += f"\n**TOTAL: {total} sessions**"
    
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Panel", callback_data="admin_panel")]
    ])
    
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")