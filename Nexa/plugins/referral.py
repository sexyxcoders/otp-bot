from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

from Nexa.database import create_user, get_user
from Nexa.database.referral import (
    add_referral,
    get_referrer,
    get_top_referrers,
    add_earning
)

from Nexa.database.deposits import approve_deposit
from Nexa.database.users import add_balance


def referral_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 Refer & Earn", callback_data="refer")],
        [InlineKeyboardButton("🏆 Leaderboard", callback_data="ref_leaderboard")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ])


@app.on_callback_query(filters.regex("^refer$"))
async def refer_cb(client, callback_query):
    user_id = callback_query.from_user.id

    # ensure user exists
    create_user(user_id, callback_query.from_user.username)

    await callback_query.answer()

    ref_link = f"https://t.me/{config.BOT_USERNAME}?start={user_id}"

    # prevent message not modified error
    try:
        await callback_query.message.edit_text(
            f"🎁 **Refer & Earn**\n\n"
            f"Invite your friends using your referral link below:\n\n"
            f"`{ref_link}`\n\n"
            f"💰 You earn **5% of deposit amount** on each first deposit by referred user.",
            reply_markup=referral_keyboard()
        )
    except Exception:
        # fallback if same message content
        await callback_query.message.reply_text(
            f"🎁 **Refer & Earn**\n\n"
            f"Invite your friends using your referral link below:\n\n"
            f"`{ref_link}`\n\n"
            f"💰 You earn **5% of deposit amount** on each first deposit by referred user.",
            reply_markup=referral_keyboard()
        )


@app.on_message(filters.private & filters.command("start"))
async def start_referral(client, message):
    # Handle referral link
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        ref_id = int(args[1])
        user_id = message.from_user.id

        # prevent self-referral
        if ref_id != user_id:
            add_referral(ref_id, user_id)

    # normal start flow will run from plugins/start.py


@app.on_callback_query(filters.regex("^ref_leaderboard$"))
async def ref_leaderboard_cb(client, callback_query):
    await callback_query.answer()

    refs = get_top_referrers(limit=10)
    if not refs:
        return await callback_query.message.edit_text("🎁 No referrals yet.")

    text = "🎁 **Top Referrers**\n\n"
    for r in refs:
        text += f"👤 `{r['user_id']}` | ₹{r['earnings']}\n"

    await callback_query.message.edit_text(text, reply_markup=referral_keyboard())