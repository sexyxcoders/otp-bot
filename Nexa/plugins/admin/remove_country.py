from Nexa.core.client import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Nexa.database.users import is_admin
from Nexa.database.sessions import get_countries, remove_country

# ----------------------
# INLINE REMOVE COUNTRY MENU
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


# ----------------------
# REMOVE COUNTRY INLINE ACTION
# ----------------------
@app.on_callback_query(filters.regex(r"^remove_country_now\|(.+)$"))
async def remove_country_now_cb(_, cq):
    if not is_admin(cq.from_user.id):
        return await cq.answer("❌ Not allowed", show_alert=True)

    country = cq.data.split("|")[1]

    # Remove country
    remove_country(country)
    await cq.answer(f"❌ Country **{country}** removed", show_alert=True)

    # Update message to reflect success
    await cq.message.edit_text(
        f"✅ Country **{country}** removed successfully.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]])
    )