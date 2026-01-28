# Nexa/plugins/__init__.py
"""
Plugin loader for Nexa Bot
Imports all user and admin plugins safely
"""

# -------------------
# User-facing plugins
# -------------------
from . import start
from . import profile
from . import deposit
from . import referral
from . import wallet
from . import order_history
from . import sessions  # user sessions

# -------------------
# Admin plugins
# -------------------
from .admin import panel
from .admin import users
from .admin import deposits
from .admin import history
from .admin import referral
from .admin import user_history
from .admin import broadcast
from .admin import sessions as admin_sessions
from .admin import stock
from .admin import country
from .admin import price
from .admin import revoke_session