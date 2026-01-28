from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import MessageNotModified

from Nexa.database.users import is_admin
from Nexa.database.sessions import (
    update_stock,
    get_stock,
    normalize_country
)


# =========================
# ADMIN STOCK PANEL
# =========================

@app.on_callback_query(filters.regex("^admin_stock$"))
async def admin_stock_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    text = (
        "📦 **Stock Management**\n\n"
        "**Command:**\n"
        "`/stock <country> <quantity>`\n\n"
        "➕ Add stock: `+10`\n"
        "➖ Reduce stock: `-5`\n\n"
        "Example:\n"
        "`/stock US 10`"
    )

    try:
        await cq.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📊 View Stock", callback_data="admin_view_stock")],
                [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
            ])
        )
    except MessageNotModified:
        pass


# =========================
# VIEW STOCK
# =========================

@app.on_callback_query(filters.regex("^admin_view_stock$"))
async def admin_view_stock(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    stocks = get_stock()

    if not stocks:
        text = "📦 No stock available."
    else:
        text = "📦 **Current Stock**\n\n"
        for c, s in stocks.items():
            text += f"🌍 {c} → `{s}` pcs\n"

    try:
        await cq.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="admin_stock")]
            ])
        )
    except MessageNotModified:
        pass


# =========================
# STOCK COMMAND
# =========================

@app.on_message(filters.private & filters.command("stock"))
async def stock_cmd(_, msg):
    if not is_admin(msg.from_user.id):
        return

    try:
        _, country, qty = msg.text.split()
        qty = int(qty)

        country = normalize_country(country)
        new_stock = update_stock(country, qty)

        if new_stock < 0:
            return await msg.reply("❌ Stock cannot go below zero.")

        await msg.reply(
            f"✅ **Stock Updated**\n\n"
            f"Country: `{country}`\n"
            f"New Stock: `{new_stock}`",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Admin Panel", callback_data="admin_panel")]
            ])
        )

    except ValueError:
        await msg.reply(
            "❌ **Usage Error**\n\n"
            "`/stock <country> <quantity>`\n"
            "Example:\n`/stock US 10`"
        )