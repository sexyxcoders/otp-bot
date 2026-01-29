from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from core.client import app
from database.sessions import mongo
import os
from dotenv import load_dotenv

load_dotenv()
ADMIN_ID = int(os.getenv("ADMIN_ID"))

@app.on_callback_query(filters.regex("^revoke_(.+)$") & filters.user(ADMIN_ID))
async def confirm_revoke(client, callback: CallbackQuery):
    session_id = callback.matches[0].group(1)
    
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ CONFIRM DELETE", callback_data=f"delete_{session_id}")],
        [InlineKeyboardButton("❌ Cancel", callback_data="admin_sessions")]
    ])
    
    await callback.message.edit_text(
        f"⚠️ **Confirm Delete Session**\n\n"
        f"Session ID: `{session_id}`\n\n"
        f"This action is **irreversible**.",
        reply_markup=kb,
        parse_mode="Markdown"
    )

@app.on_callback_query(filters.regex("^delete_(.+)$") & filters.user(ADMIN_ID))
async def delete_session(client, callback: CallbackQuery):
    session_id = callback.matches[0].group(1)
    result = await mongo.db.sessions.delete_one({"_id": session_id})
    
    if result.deleted_count:
        await callback.message.edit_text(
            f"✅ **Session Deleted!**\n\n"
            f"ID: `{session_id}`",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📱 Sessions", callback_data="admin_sessions")]
            ]),
            parse_mode="Markdown"
        )
    else:
        await callback.message.edit_text("❌ Session not found!")