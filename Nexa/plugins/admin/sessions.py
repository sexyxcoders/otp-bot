from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import add_session, remove_session


@app.on_callback_query(filters.regex("^admin_sessions$"))
async def admin_sessions_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    text = (
        "📲 **Session Management**\n\n"
        "To add a session:\n"
        "`/addsession Country | Price | Stock | SessionString | 2FA(True/False)`\n\n"
        "To remove a session:\n"
        "`/removesession [session_id]`"
    )
    
    await cq.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )


@app.on_callback_query(filters.regex("^add_session$"))
async def add_session_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)
        
    await cq.message.edit_text(
        "➕ **Add Session**\n\n"
        "To add a new session, use the command:\n"
        "`/addsession Country | Price | Stock | String | 2FA`\n\n"
        "Example:\n`/addsession India | 15 | 1 | 1B... | False`",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )


@app.on_callback_query(filters.regex("^remove_session$"))
async def remove_session_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)
        
    await cq.message.edit_text(
        "❌ **Remove Session**\n\n"
        "To remove a session, use the command:\n"
        "`/removesession [Session_ID]`",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )


@app.on_message(filters.command("addsession"))
async def add_session_cmd(_, msg):
    if not is_admin(msg.from_user.id):
        return

    try:
        # /addsession Country | Price | Stock | String | 2FA
        args = msg.text.split(" ", 1)[1].split("|")
        if len(args) < 4:
            raise ValueError
            
        country = args[0].strip()
        price = float(args[1].strip())
        stock = int(args[2].strip())
        string_session = args[3].strip()
        two_step = args[4].strip().lower() == "true" if len(args) > 4 else False
        
        add_session(country, price, stock, string_session, two_step, msg.from_user.id)
        
        await msg.reply(
            f"✅ **Session Added**\n\nCountry: {country}\nPrice: {price}\nStock: {stock}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Admin Panel", callback_data="admin_panel")]])
        )
    except Exception:
        await msg.reply(
            "❌ **Error**\n\nUsage:\n`/addsession Country | Price | Stock | String | 2FA`",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Admin Panel", callback_data="admin_panel")]])
        )


@app.on_message(filters.command("removesession"))
async def remove_session_cmd(_, msg):
    if not is_admin(msg.from_user.id):
        return

    try:
        session_id = msg.text.split(maxsplit=1)[1]
        remove_session(session_id)
        await msg.reply(
            "✅ **Session Removed**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Admin Panel", callback_data="admin_panel")]])
        )
    except IndexError:
        await msg.reply(
            "❌ **Error**\n\nUsage: `/removesession [session_id]`",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Admin Panel", callback_data="admin_panel")]])
        )