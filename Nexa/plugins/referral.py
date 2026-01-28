from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

from Nexa.database import create_user
from Nexa.database.referral import add_referral, get_top_referrers


# ---------------------------
# REFERRAL KEYBOARD
# ---------------------------
def referral_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 Refer & Earn", callback_data="refer")],
        [InlineKeyboardButton("🏆 Leaderboard", callback_data="ref_leaderboard")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
    ])


# ---------------------------
# REFER BUTTON
# ---------------------------
@app.on_callback_query(filters.regex("^refer$"))
async def refer_cb(client, cq):
    user_id = cq.from_user.id
    create_user(user_id, cq.from_user.username or "")

    ref_link = f"https://t.me/{config.BOT_USERNAME}?start={user_id}"

    text = (
        f"🎁 **Refer & Earn**\n\n"
        f"Invite your friends using your referral link:\n\n"
        f"`{ref_link}`\n\n"
        f"💰 Earn **5% of deposit amount** on each first deposit by referred users."
    )

    # Edit message safely
    try:
        await cq.message.edit_text(text, reply_markup=referral_keyboard())
    except:
        await cq.message.reply_text(text, reply_markup=referral_keyboard())

    await cq.answer()


# ---------------------------
# REFERRAL LEADERBOARD
# ---------------------------
@app.on_callback_query(filters.regex("^ref_leaderboard$"))
async def ref_leaderboard_cb(client, cq):
    await cq.answer()

    refs = get_top_referrers(limit=10)
    if not refs:
        return await cq.message.edit_text("🎁 No referrals yet.", reply_markup=referral_keyboard())

    text = "🎁 **Top Referrers**\n\n"
    for r in refs:
        text += f"👤 `{r['user_id']}` | 💰 ₹{r['earnings']}\n"

    await cq.message.edit_text(text, reply_markup=referral_keyboard())


# ---------------------------
# HANDLE /start REFERRAL ARG
# ---------------------------
@app.on_message(filters.private & filters.command("start"))
async def start_referral(client, message):
    args = message.text.split()
    user_id = message.from_user.id
    create_user(user_id, message.from_user.username or "")

    if len(args) > 1 and args[1].isdigit():
        ref_id = int(args[1])

        # Prevent self-referral
        if ref_id != user_id:
            add_referral(ref_id, user_id)