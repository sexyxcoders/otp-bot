from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
import config

from Nexa.database import (
    create_user, update_username, get_available_countries,
    get_balance, deduct_balance, add_balance, get_price, assign_session_to_user,
    create_order, get_total_orders, get_referrer_earnings, is_admin
)


def start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📲 Buy Number", callback_data="buy_sessions")],
        [
            InlineKeyboardButton("👤 Profile", callback_data="profile"),
            InlineKeyboardButton("💰 Wallet", callback_data="wallet")
        ],
        [
            InlineKeyboardButton("💳 Deposit", callback_data="deposit"),
            InlineKeyboardButton("📜 History", callback_data="history")
        ],
        [
            InlineKeyboardButton("🎁 Refer & Earn", callback_data="refer"),
            InlineKeyboardButton("🧑‍💻 Support", callback_data="support")
        ]
    ])


async def must_join(client, user_id, chat_id, edit_msg=None):
    """
    Checks if user joined required channel.
    Sends OR edits join message safely.
    """
    if not getattr(config, "MUST_JOIN", None):
        return True

    try:
        await client.get_chat_member(config.MUST_JOIN, user_id)
        return True

    except UserNotParticipant:
        text = "⚠️ **You must join our channel to use this bot**"
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📢 Join Channel",
                    url=f"https://t.me/{config.MUST_JOIN}"
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ Joined",
                    callback_data="check_join"
                )
            ]
        ])

        if edit_msg:
            await edit_msg.edit_text(text, reply_markup=keyboard)
        else:
            await client.send_message(chat_id, text, reply_markup=keyboard)

        return False


@app.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    user = message.from_user

    # MUST JOIN CHECK
    if not await must_join(client, user.id, message.chat.id):
        return

    # CREATE / UPDATE USER
    create_user(user.id, user.username or "")
    update_username(user.id, user.username or "")

    keyboard = start_keyboard()
    if is_admin(user.id):
        keyboard.inline_keyboard.append([InlineKeyboardButton("👑 Admin Panel", callback_data="admin_panel")])

    await message.reply_text(
        "✨ **Welcome to Nexa Number Market**\n\n"
        "Buy virtual numbers instantly at best prices 🚀\n\n"
        "Select an option below 👇",
        reply_markup=keyboard
    )


@app.on_callback_query(filters.regex("^buy_sessions$"))
async def buy_sessions_cb(client, cq):
    countries = get_available_countries()
    
    if not countries:
        return await cq.message.edit_text(
            "❌ **No Stock Available**\n\nPlease check back later.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]])
        )
        
    buttons = []
    for c in countries:
        buttons.append([InlineKeyboardButton(f"{c['country']} - ₹{c['price']} ({c['stock']})", callback_data=f"buy_country_{c['country']}")])
    
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="main_menu")])
    
    await cq.message.edit_text(
        "📲 **Select a Country**\n\nChoose a country to buy a number:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex("^buy_country_"))
async def buy_country_cb(client, cq):
    country = cq.data.split("_", 2)[2]
    user_id = cq.from_user.id
    
    price = get_price(country)
    if not price:
        return await cq.answer("❌ Price not found", show_alert=True)
        
    # Deduct balance first to prevent race conditions
    if not deduct_balance(user_id, price):
        return await cq.answer(f"❌ Insufficient Balance! Need ₹{price}", show_alert=True)
        
    # Try to assign session
    session = assign_session_to_user(user_id, country)
    if not session:
        # Refund if out of stock
        add_balance(user_id, price)
        return await cq.answer("❌ Out of Stock", show_alert=True)
        
    # Create order record
    order_id = create_order(user_id, session)
    
    await cq.message.edit_text(
        f"✅ **Order Successful!**\n\n"
        f"🆔 Order ID: `{order_id}`\n"
        f"🌍 Country: {country}\n"
        f"💰 Price: ₹{price}\n\n"
        f"⚠️ **Session String:**\n`{session['string_session']}`\n\n"
        f"⏳ Expires in 30 mins. OTPs will be sent here.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]])
    )


@app.on_callback_query(filters.regex("^profile$"))
async def profile_cb(client, cq):
    user_id = cq.from_user.id
    balance = get_balance(user_id)
    orders_count = get_total_orders(user_id)
    
    await cq.message.edit_text(
        f"👤 **My Profile**\n\n"
        f"🆔 ID: `{user_id}`\n"
        f"💰 Balance: ₹{balance}\n"
        f"📦 Total Orders: {orders_count}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]])
    )


@app.on_callback_query(filters.regex("^wallet$"))
async def wallet_cb(client, cq):
    user_id = cq.from_user.id
    balance = get_balance(user_id)
    
    await cq.message.edit_text(
        f"💰 **My Wallet**\n\n"
        f"Current Balance: **₹{balance}**\n\n"
        "To deposit funds, click the button below.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 Deposit", callback_data="deposit")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
        ])
    )


@app.on_callback_query(filters.regex("^refer$"))
async def refer_cb(client, cq):
    user_id = cq.from_user.id
    link = f"https://t.me/{config.BOT_USERNAME}?start={user_id}"
    earnings = get_referrer_earnings(user_id)
    
    await cq.message.edit_text(
        f"🎁 **Refer & Earn**\n\n"
        f"Share your link and earn 5% of your friends' deposits!\n\n"
        f"🔗 Link:\n`{link}`\n\n"
        f"💰 Total Earnings: ₹{earnings}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]])
    )


@app.on_callback_query(filters.regex("^(history|support)$"))
async def main_features_cb(client, cq):
    data = cq.data
    
    if data == "history":
        text = "📜 **History**\n\nNo recent activity found."
    elif data == "support":
        text = "🧑‍💻 **Support**\n\nIf you need help, please contact the admin."
        
    buttons = [[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]
    if data == "support":
        buttons.insert(0, [InlineKeyboardButton("💬 Contact Admin", url=f"https://t.me/{config.BOT_USERNAME}")])

    await cq.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex("^check_join$"))
async def check_join_cb(client, cq):
    await cq.answer()

    if not await must_join(
        client,
        cq.from_user.id,
        cq.message.chat.id,
        edit_msg=cq.message
    ):
        return

    await cq.message.edit_text(
        "✅ **Access granted!**\n\nChoose an option below 👇",
        reply_markup=start_keyboard()
    )


@app.on_callback_query(filters.regex("^main_menu$"))
async def main_menu_cb(client, cq):
    await cq.answer()

    keyboard = start_keyboard()
    if is_admin(cq.from_user.id):
        keyboard.inline_keyboard.append([InlineKeyboardButton("👑 Admin Panel", callback_data="admin_panel")])

    await cq.message.edit_text(
        "✨ **Welcome to Nexa Number Market**\n\n"
        "Buy virtual numbers instantly at best prices 🚀\n\n"
        "Select an option below 👇",
        reply_markup=keyboard
    )