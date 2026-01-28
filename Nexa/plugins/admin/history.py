from datetime import datetime
from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.mongo import orders, sessions

ORDERS_PER_PAGE = 10  # Number of orders per page


def format_orders_text(order_list, page, total_pages):
    text = f"📜 **Order & Session History** | Page {page}/{total_pages}\n\n"
    for order in order_list:
        order_id = order.get("order_id", "N/A")[:8]
        status_icon = "✅" if order.get("status") == "active" else "❌"
        country = order.get("country", "Unknown")
        price = order.get("price", 0)
        user_id = order.get("user_id", "Unknown")
        created_at = order.get("created_at")
        date_str = created_at.strftime("%Y-%m-%d %H:%M") if isinstance(created_at, datetime) else "N/A"

        # Check if user has revoked sessions
        revoked_sessions_count = sessions.count_documents({"user_id": user_id, "revoked": True})

        # Check stock/session usage
        total_sessions = sessions.count_documents({"user_id": user_id})

        text += (
            f"{status_icon} `{order_id}` | {country} | ₹{price}\n"
            f"👤 `{user_id}` | 📅 {date_str}\n"
            f"📦 Sessions Used: {total_sessions} | ⚠️ Revoked: {revoked_sessions_count}\n\n"
        )
    return text


def build_orders_keyboard(page, total_pages):
    buttons = []

    # Pagination buttons
    row = []
    if page > 1:
        row.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"admin_history_{page-1}"))
    if page < total_pages:
        row.append(InlineKeyboardButton("Next ➡️", callback_data=f"admin_history_{page+1}"))
    if row:
        buttons.append(row)

    # Refresh + Back buttons
    buttons.append([
        InlineKeyboardButton("🔄 Refresh", callback_data=f"admin_history_{page}"),
        InlineKeyboardButton("🔙 Back", callback_data="admin_panel")
    ])
    return InlineKeyboardMarkup(buttons)


@app.on_callback_query(filters.regex(r"^admin_history(?:_\d+)?$"))
async def admin_history_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    # Extract page number
    data = cq.data
    page = int(data.split("_")[2]) if "_" in data and data.split("_")[2].isdigit() else 1

    total_orders = orders.count_documents({})
    if total_orders == 0:
        return await cq.message.edit_text(
            "📜 **Order & Session History**\n\nNo orders found.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
        )

    total_pages = (total_orders + ORDERS_PER_PAGE - 1) // ORDERS_PER_PAGE
    if page > total_pages:
        page = total_pages

    # Fetch orders for this page
    skip_count = (page - 1) * ORDERS_PER_PAGE
    order_list = list(orders.find().sort("created_at", -1).skip(skip_count).limit(ORDERS_PER_PAGE))

    text = format_orders_text(order_list, page, total_pages)
    keyboard = build_orders_keyboard(page, total_pages)

    await cq.message.edit_text(text, reply_markup=keyboard)