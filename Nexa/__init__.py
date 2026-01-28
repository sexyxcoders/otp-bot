# Nexa/__init__.py

# ----------------------------
# Core
# ----------------------------
from .core.client import app
from .core.otp_manager import *

# ----------------------------
# Database
# ----------------------------
from .database import (
    users,
    sessions,
    otp_codes,
    deposits,
    orders,
    referral
)

# ----------------------------
# Plugins
# ----------------------------
import Nexa.plugins