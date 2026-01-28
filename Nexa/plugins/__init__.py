# Root plugins package
# Pyrogram will auto-load all plugin files from this folder

# Import root plugins explicitly (optional, for clarity)
from . import deposit
from . import referral
from . import order_history
from . import sessions
from . import wallet
from . import profile
from . import start
  # if you have a test plugin

# Do NOT import admin plugins here; keep root & admin separate

print(">>> ROOT PLUGINS LOADED <<<")