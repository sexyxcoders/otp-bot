from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import revoke_session


@app.on_message(filters.command("revoke"))
async def revoke_cmd(_, msg):
    if not is_admin(msg.from_user.id):
        return

    try:
        session_id = msg.text.split(maxsplit=1)[1]
        revoke_session(session_id, admin_id=msg.from_user.id)
        await msg.reply(
            f"❌ Session `{session_id}` revoked successfully.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Admin Panel", callback_data="admin_panel")]])
        )
    except IndexError:
        await msg.reply("❌ Usage: `/revoke [session_id]`")