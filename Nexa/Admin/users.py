from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import get_user, create_user

@app.on_callback_query(filters.regex("^admin_users$"))
async def admin_users_cb(client, cq):
    await cq.answer()
    users_list = list(get_user())  # Fetch all users

    if not users_list:
        return await cq.message.edit_text("❌ No users found")

    text = "👥 **All Users**\n\n"
    for u in users_list[:50]:  # Limit first 50
        text += f"🆔 `{u['user_id']}` | Balance: ₹{u.get('balance', 0)}\n"

    await cq.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )