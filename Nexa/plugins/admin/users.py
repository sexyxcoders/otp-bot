from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin, add_balance, deduct_balance, get_user
from Nexa.database.mongo import users


@app.on_callback_query(filters.regex("^admin_users$"))
async def admin_users_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)
    
    total_users = users.count_documents({})
    text = (
        f"👥 **User Management**\n\n"
        f"Total Users: `{total_users}`\n\n"
        "To manage balance:\n"
        "`/add_balance [user_id] [amount]`\n"
        "`/sub_balance [user_id] [amount]`\n\n"
        "To view user info:\n"
        "`/user [user_id]`"
    )
    
    await cq.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Balance", callback_data="admin_add_balance"),
             InlineKeyboardButton("➖ Sub Balance", callback_data="admin_sub_balance")],
            [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
        ])
    )


@app.on_callback_query(filters.regex("^admin_(add|sub)_balance$"))
async def admin_balance_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)
    
    action = cq.data.split("_")[1]
    command = "/add_balance" if action == "add" else "/sub_balance"
    
    await cq.message.edit_text(
        f"💰 **{action.title()} Balance**\n\n"
        f"Usage:\n`{command} [user_id] [amount]`",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_users")]])
    )


@app.on_message(filters.command(["add_balance", "addbalance"]))
async def add_balance_cmd(_, msg):
    if not is_admin(msg.from_user.id):
        return

    try:
        _, user_id, amount = msg.text.split()
        user_id = int(user_id)
        amount = float(amount)
        
        add_balance(user_id, amount)
        await msg.reply(
            f"✅ Added ₹{amount} to user `{user_id}`",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Admin Panel", callback_data="admin_panel")]])
        )
    except ValueError:
        await msg.reply("❌ Usage: `/add_balance [user_id] [amount]`")


@app.on_message(filters.command(["sub_balance", "subbalance"]))
async def sub_balance_cmd(_, msg):
    if not is_admin(msg.from_user.id):
        return

    try:
        _, user_id, amount = msg.text.split()
        user_id = int(user_id)
        amount = float(amount)
        
        if deduct_balance(user_id, amount):
            await msg.reply(
                f"✅ Deducted ₹{amount} from user `{user_id}`",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Admin Panel", callback_data="admin_panel")]])
            )
        else:
            await msg.reply("❌ Insufficient balance or user not found.")
    except ValueError:
        await msg.reply("❌ Usage: `/sub_balance [user_id] [amount]`")


@app.on_message(filters.command("user"))
async def user_info_cmd(_, msg):
    if not is_admin(msg.from_user.id):
        return
        
    try:
        user_id = int(msg.text.split()[1])
        user = get_user(user_id)
        if not user:
            return await msg.reply("❌ User not found")
            
        text = (
            f"👤 **User Info**\n\n"
            f"ID: `{user['user_id']}`\n"
            f"Username: @{user.get('username', 'None')}\n"
            f"Balance: ₹{user.get('balance', 0)}\n"
            f"Joined: `{user.get('created_at', 'N/A')}`"
        )
        await msg.reply(text)
    except IndexError:
        await msg.reply("❌ Usage: `/user [user_id]`")