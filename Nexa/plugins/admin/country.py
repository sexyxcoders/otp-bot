from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import add_country, remove_country


@app.on_message(filters.command("addcountry"))
async def add_country_cmd(_, msg):
    if not is_admin(msg.from_user.id):
        return
    country = msg.text.split(maxsplit=1)[1]
    add_country(country)
    await msg.reply(f"✅ Country **{country}** added")


@app.on_message(filters.command("removecountry"))
async def remove_country_cmd(_, msg):
    if not is_admin(msg.from_user.id):
        return
    country = msg.text.split(maxsplit=1)[1]
    remove_country(country)
    await msg.reply(f"❌ Country **{country}** removed")


@app.on_callback_query(filters.regex("^add_country$"))
async def add_country_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)
        
    await cq.message.edit_text(
        "➕ **Add Country**\n\n"
        "To add a new country, use the command:\n"
        "`/addcountry [Name]`\n\n"
        "Example: `/addcountry India`",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )


@app.on_callback_query(filters.regex("^remove_country$"))
async def remove_country_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)
        
    await cq.message.edit_text(
        "❌ **Remove Country**\n\n"
        "To remove a country, use the command:\n"
        "`/removecountry [Name]`\n\n"
        "Example: `/removecountry India`",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )