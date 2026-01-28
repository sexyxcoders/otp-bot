# Nexa/__init__.py

# Initialize the Pyrogram client (app) and core functionality
from .core.client import app
from .core.otp_manager import *
from .core.storage import *
from .core.client import *  # optional if you want global access

# Do NOT import plugins here, import them in bot.py after app is defined
# This prevents circular imports and startup errors