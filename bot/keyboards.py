from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def country_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇮🇳 India", callback_data="buy_IN")],
        [InlineKeyboardButton("🇺🇸 USA", callback_data="buy_US")]
    ])