from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from core.client import app
from database.sessions import mongo
import os
from dotenv import load_dotenv

load_dotenv()
ADMIN_ID = int(os.getenv("ADMIN_ID"))

@app.on_callback_query(filters.regex("^admin_sessions$") & filters.user(ADMIN_ID))
async def admin_sessions(client, callback: CallbackQuery):
    sessions = await mongo.db.sessions.find({"stock": {"$gt": 0}}).limit(15).to_list(None)
    
    text = "📱 **ACTIVE SESSIONS:**\n\n"
    kb = []
    
    for session in sessions:
        sid = str(session["_id"])[:8]
        text += f"`{session['session_string'][:10]}...`\n"
        text += f"🌍 {session['country']} | 📊 {session['stock']} | 💰 ${session['price']}\n\n"
        
        kb.append([InlineKeyboardButton(
            f"🚫 Revoke {sid}",
            callback_data=f"revoke_{str(session['_id'])}"
        )])
    
    kb.append([InlineKeyboardButton("🔙 Panel", callback_data="admin_panel")])
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")