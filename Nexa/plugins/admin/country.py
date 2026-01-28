from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import get_countries, add_country, remove_country

# ----------------------
# COUNTRY MANAGEMENT MENU
# ----------------------
@app.on_callback_query(filters.regex("^admin_countries$"))
async def admin_countries_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    countries = get_countries()
    text = "🌍 **Countries Management**\n\n"

    if not countries:
        text += "No countries added yet."
    else:
        for c in countries:
            text += f"• {c['name']}\n"

    # Buttons
    buttons = [
        [InlineKeyboardButton("➕ Add Country", callback_data="add_country")],
        [InlineKeyboardButton("❌ Remove Country", callback_data="remove_country")],
        [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
    ]

    await cq.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))


# ----------------------
# ADD COUNTRY INLINE
# ----------------------
@app.on_callback_query(filters.regex("^add_country$"))
async def add_country_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    # Pre-defined common countries (optional)
    common_countries = ["India", "USA", "UK", "Canada", "Germany"]

    buttons = [[InlineKeyboardButton(c, callback_data=f"add_country_now|{c}")] for c in common_countries]
    buttons.append([InlineKeyboardButton("➕ Add New Country", callback_data="add_country_new")])
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="admin_panel")])

    await cq.message.edit_text(
        "➕ **Add Country**\n\n"
        "Select a country to add from the list or add a new one manually:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(r"^add_country_now\|(.+)$"))
async def add_country_now_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    country = cq.data.split("|")[1]
    add_country(country)
    await cq.answer(f"✅ Country **{country}** added", show_alert=True)

    await cq.message.edit_text(
        f"✅ Country **{country}** added successfully.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )


# Admin types a new country manually
@app.on_callback_query(filters.regex("^add_country_new$"))
async def add_country_new_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    await cq.message.edit_text(
        "✏️ **Add New Country**\n\n"
        "Send the country name in this chat and it will be added automatically.",
    )


@app.on_message(filters.private)
async def handle_add_country_msg(_, msg):
    if not is_admin(msg.from_user.id):
        return

    text = msg.text.strip()
    if not text:
        return
    if text.lower() == "/cancel":
        return await msg.reply("❌ Action cancelled.")

    # Add new country manually
    add_country(text)
    await msg.reply(f"✅ Country **{text}** added successfully.")


# ----------------------
# REMOVE COUNTRY INLINE
# ----------------------
@app.on_callback_query(filters.regex("^remove_country$"))
async def remove_country_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    countries = get_countries()
    if not countries:
        return await cq.message.edit_text(
            "❌ No countries available to remove.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
        )

    text = "❌ **Remove Country**\n\nSelect a country to remove:"

    # 1 column of buttons
    buttons = [[InlineKeyboardButton(c['name'], callback_data=f"remove_country_now|{c['name']}")] for c in countries]
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="admin_panel")])

    await cq.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex(r"^remove_country_now\|(.+)$"))
async def remove_country_now_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    country = cq.data.split("|")[1]
    remove_country(country)
    await cq.answer(f"❌ Country **{country}** removed", show_alert=True)

    await cq.message.edit_text(
        f"✅ Country **{country}** removed successfully.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )