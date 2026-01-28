from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin

def admin_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🌍 Countries", callback_data="admin_countries"),
            InlineKeyboardButton("➕ Add Country", callback_data="add_country")
        ],
        [
            InlineKeyboardButton("❌ Remove Country", callback_data="remove_country"),
            InlineKeyboardButton("💰 Prices", callback_data="admin_prices")
        ],
        [
            InlineKeyboardButton("📲 Sessions", callback_data="admin_sessions"),
            InlineKeyboardButton("➕ Add Session", callback_data="add_session")
        ],
        [
            InlineKeyboardButton("❌ Remove Session", callback_data="remove_session"),
            InlineKeyboardButton("🛑 Revoke Session", callback_data="admin_revoke_session")
        ],
        [
            InlineKeyboardButton("📦 Stock", callback_data="admin_stock"),
            InlineKeyboardButton("📊 Users", callback_data="admin_users")
        ],
        [
            InlineKeyboardButton("🧾 Orders", callback_data="admin_history"),
            InlineKeyboardButton("📌 Deposits", callback_data="admin_deposits")
        ],
        [
            InlineKeyboardButton("🎁 Referral", callback_data="admin_referral"),
            InlineKeyboardButton("📣 Broadcast", callback_data="admin_broadcast")
        ],
        [
            InlineKeyboardButton("➕ Add Balance", callback_data="admin_add_balance"),
            InlineKeyboardButton("➖ Sub Balance", callback_data="admin_sub_balance")
        ],
        [
            InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")
        ]
    ])

@app.on_callback_query(filters.regex("^admin_panel$"))
async def admin_panel_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)
    await cq.message.edit_text("👑 **Admin Panel**", reply_markup=admin_keyboard())
    await cq.answer()

@app.on_message(filters.private & filters.command(["admin", "panel"]))
async def admin_panel_cmd(_, message):
    if not is_admin(message.from_user.id):
        return await message.reply_text("❌ You are not an admin")
    await message.reply_text("👑 **Admin Panel**", reply_markup=admin_keyboard())