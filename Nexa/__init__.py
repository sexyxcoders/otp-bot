# Nexa/__init__.py

# Only core imports, no * imports from client
from .core.client import app
from .core.otp_manager import *
from .core.storage import *

# Do NOT import plugins here, they should be imported in bot.py AFTER app is defined