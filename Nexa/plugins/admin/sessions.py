from uuid import uuid4
from datetime import datetime

from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import MessageNotModified

from Nexa.database.users import is_admin
from Nexa.database.sessions import (
    add_session,
    remove_session,
    list_sessions,
    normalize_country
)


# =========================
# ADMIN SESSION PANEL
# =========================

@app.on_callback_query(filters.regex("^admin_sessions$"))
async def admin_sessions_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    text = (
        "📲 **Session Management**\n\n"
        "**Add session:**\n"
        "`/addsession Country | Price | Stock | String | 2FA(True/False)`\n\n"
        "**Remove session:**\n"
        "`/removesession <session_id>`\n\n"
        "**View sessions:**\n"
        "`/sessions`"
    )

    try:
        await cq.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 View Sessions", callback_data="admin_list_sessions")],
                [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
            ])
        )
    except MessageNotModified:
        pass


# =========================
# LIST SESSIONS
# =========================

@app.on_callback_query(filters.regex("^admin_list_sessions$"))
async def admin_list_sessions(_, cq):
    if not is_admin(cq.from_user.id):
        return

    sessions = list_sessions()

    if not sessions:
        text = "📭 No sessions available."
    else:
        text = "📋 **Available Sessions**\n\n"
        for s in sessions:
            text += (
                f"🆔 `{s['session_id']}`\n"
                f"🌍 {s['country']} | 💰 ₹{s['price']} | 📦 {s['stock']}\n"
                f"🔐 2FA: {s['two_step']}\n\n"
            )

    try:
        await cq.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="admin_sessions")]
            ])
        )
    except MessageNotModified:
        pass


# =========================
# ADD SESSION COMMAND
# =========================

@app.on_message(filters.private & filters.command("addsession"))
async def add_session_cmd(_, msg):
    if not is_admin(msg.from_user.id):
        return

    try:
        # /addsession Country | Price | Stock | String | 2FA
        raw = msg.text.split(" ", 1)[1]
        args = [x.strip() for x in raw.split("|")]

        if len(args) < 4:
            raise ValueError

        country = normalize_country(args[0])
        price = float(args[1])
        stock = int(args[2])
        string_session = args[3]
        two_step = args[4].lower() == "true" if len(args) > 4 else False

        session_id = str(uuid4())[:8]

        add_session(
            session_id=session_id,
            country=country,
            price=price,
            stock=stock,
            string_session=string_session,
            two_step=two_step,
            added_by=msg.from_user.id,
            created_at=datetime.utcnow()
        )

        await msg.reply(
            f"✅ **Session Added**\n\n"
            f"🆔 `{session_id}`\n"
            f"🌍 {country}\n"
            f"💰 ₹{price}\n"
            f"📦 {stock}\n"
            f"🔐 2FA: {two_step}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Admin Panel", callback_data="admin_panel")]
            ])
        )

    except Exception:
        await msg.reply(
            "❌ **Invalid Format**\n\n"
            "`/addsession Country | Price | Stock | String | 2FA`\n\n"
            "Example:\n"
            "`/addsession US | 35 | 5 | 1B... | False`"
        )


# =========================
# REMOVE SESSION COMMAND
# =========================

@app.on_message(filters.private & filters.command("removesession"))
async def remove_session_cmd(_, msg):
    if not is_admin(msg.from_user.id):
        return

    try:
        session_id = msg.text.split(maxsplit=1)[1].strip()
        removed = remove_session(session_id)

        if not removed:
            return await msg.reply("❌ Session not found.")

        await msg.reply(
            f"🗑 **Session Removed**\n\nID: `{session_id}`",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Admin Panel", callback_data="admin_panel")]
            ])
        )

    except IndexError:
        await msg.reply("❌ Usage: `/removesession <session_id>`")