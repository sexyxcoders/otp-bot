from .users import (
    create_user,
    update_username,
    get_user,
    get_balance,
    add_balance,
    deduct_balance,
    is_admin
)

from .orders import (
    create_order,
    get_order,
    get_total_orders,
    get_user_orders,
    update_order_status
)

from .deposits import (
    add_deposit,
    get_pending_deposits,
    update_deposit_status,
    get_deposit_by_id,
    approve_deposit
)

from .referral import (
    add_referral,
    add_earning,
    get_referrer,
    get_referrer_earnings,
    get_top_referrers,
    reset_referral_earnings
)

# -----------------------
# Sessions
# -----------------------
from .sessions import (
    add_session,
    remove_session,
    update_stock,
    get_session,
    get_available_countries,
    get_country_info,
    revoke_session,
    add_country,
    remove_country,
    get_countries,
    set_price,
    get_price,
    list_sessions,
    normalize_country,
    assign_session_to_user   # ✅ added here
)

from .otp_codes import (
    store_otp,
    get_latest_otp,
    mark_otp_used
)