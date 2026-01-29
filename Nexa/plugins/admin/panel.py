from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.client import app
import os
from dotenv import load_dotenv

load_dotenv()
ADMIN_ID = int(os.getenv("ADMIN_ID"))

@app.on_message(filters.command("admin") & filters.user(ADMIN_ID))
@app.on_callback_query(filters.regex("^admin_panel$") & filters.user(ADMIN_ID))
async def admin_panel(client, message):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Stock", callback_data="admin_stock")],
        [InlineKeyboardButton("➕ Add Session", callback_data="admin_add_session")],
        [InlineKeyboardButton("📱 Sessions", callback_data="admin_sessions")],
        [InlineKeyboardButton("💰 Add Balance", callback_data="admin_add_balance")],
        [InlineKeyboardButton("🌍 Countries", callback_data="admin_countries")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")]
    ])
    
    text = "🔧 **ADMIN PANEL**\n\n📊 Stock | ➕ Sessions | 💰 Balance"
    
    if hasattr(message, 'edit_text'):
        await message.edit_text(text, reply_markup=kb)
    else:
        await message.reply_text(text, reply_markup=kb)