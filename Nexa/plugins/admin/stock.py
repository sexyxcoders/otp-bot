from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import update_stock


@app.on_callback_query(filters.regex("^admin_stock$"))
async def admin_stock_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)
        
    await cq.message.edit_text(
        "📦 **Stock Management**\n\n"
        "To update stock manually:\n"
        "`/stock [country] [quantity]`\n"
        "(Use negative quantity to decrease)",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )


@app.on_message(filters.command("stock"))
async def stock_cmd(_, msg):
    if not is_admin(msg.from_user.id):
        return

    try:
        _, country, qty = msg.text.split()
        update_stock(country, int(qty))
        await msg.reply(
            f"📦 **Stock Updated**\n\nCountry: {country}\nChange: {qty}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Admin Panel", callback_data="admin_panel")]])
        )
    except ValueError:
        await msg.reply(
            "❌ **Error**\n\nUsage: `/stock [country] [quantity]`",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Admin Panel", callback_data="admin_panel")]])
        )