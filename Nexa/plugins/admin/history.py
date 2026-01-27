from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.mongo import orders
from datetime import datetime


@app.on_callback_query(filters.regex("^admin_history$"))
async def admin_history_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)
    
    # Fetch last 10 orders
    recent_orders = list(orders.find().sort("created_at", -1).limit(10))
    
    if not recent_orders:
        return await cq.message.edit_text(
            "📜 **Order History**\n\nNo orders found.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
        )
    
    text = "📜 **Recent Orders**\n\n"
    for order in recent_orders:
        status = "✅" if order.get("status") == "active" else "❌"
        date_val = order.get("created_at")
        if isinstance(date_val, datetime):
            date_str = date_val.strftime("%Y-%m-%d %H:%M")
        else:
            date_str = "N/A"
            
        text += f"{status} `{order.get('order_id', 'N/A')[:8]}` | {order.get('country', 'Unknown')} | ₹{order.get('price', 0)}\n"
        text += f"👤 `{order.get('user_id', 'Unknown')}` | 📅 {date_str}\n\n"
        
    await cq.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )
