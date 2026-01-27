from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import get_countries


def admin_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌍 Countries", callback_data="admin_countries"),
         InlineKeyboardButton("➕ Add Country", callback_data="add_country")],

        [InlineKeyboardButton("❌ Remove Country", callback_data="remove_country")],

        [InlineKeyboardButton("💰 Prices", callback_data="admin_prices")],

        [InlineKeyboardButton("📲 Sessions", callback_data="admin_sessions"),
         InlineKeyboardButton("➕ Add Session", callback_data="add_session")],

        [InlineKeyboardButton("❌ Remove Session", callback_data="remove_session")],

        [InlineKeyboardButton("📦 Stock", callback_data="admin_stock")],

        [InlineKeyboardButton("📊 Users", callback_data="admin_users"),
         InlineKeyboardButton("🧾 Orders", callback_data="admin_history")],

        [InlineKeyboardButton("📌 Deposits", callback_data="admin_deposits"),
         InlineKeyboardButton("🎁 Referral", callback_data="admin_referral")],

        [InlineKeyboardButton("➕ Add Balance", callback_data="admin_add_balance"),
         InlineKeyboardButton("➖ Sub Balance", callback_data="admin_sub_balance")],

        [InlineKeyboardButton("📣 Broadcast", callback_data="admin_broadcast")],

        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ])


# 🔘 CALLBACK OPEN
@app.on_callback_query(filters.regex("^admin_panel$"))
async def admin_panel_cb(_, cq):
    await cq.answer()

    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    await cq.message.edit_text("👑 **Admin Panel**", reply_markup=admin_keyboard())


# 🔑 COMMAND OPEN (/admin OR /panel)
@app.on_message(
    filters.private
    & filters.command(["admin", "panel"])
)
async def admin_panel_cmd(_, message):
    if not is_admin(message.from_user.id):
        return await message.reply_text("❌ You are not an admin")

    await message.reply_text(
        "👑 **Admin Panel**",
        reply_markup=admin_keyboard()
    )


@app.on_callback_query(filters.regex("^admin_countries$"))
async def admin_countries_cb(_, cq):
    countries = get_countries()
    text = "🌍 **Countries List**\n\n"
    if not countries:
        text += "No countries added."
    else:
        for c in countries:
            text += f"• {c['name']}\n"
    
    await cq.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )