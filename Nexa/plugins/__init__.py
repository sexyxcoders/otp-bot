# Root plugins package
# Only import root modules here
# Do NOT import admin plugins

from . import deposit
from . import referral
from . import order_history
from . import sessions
from . import wallet
from . import profile
from . import start

print(">>> ROOT PLUGINS LOADED <<<")