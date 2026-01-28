# Nexa/plugins/__init__.py

# ✅ Load regular user plugins
from . import start
from . import otp
from . import balance  # if you have balance.py for non-admin commands

# ✅ Load admin plugins
from .admin import panel
from .admin import country
from .admin import price
from .admin import sessions
from .admin import revoke_session
from .admin import stock
from .admin import broadcast