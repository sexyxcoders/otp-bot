from datetime import datetime
from Nexa.database.otp_codes import (
    store_otp,
    get_latest_otp,
    mark_otp_used
)
from Nexa.database.sessions import get_session


def is_session_valid(session):
    if not session:
        return False
    if not session.get("active"):
        return False
    if session.get("revoked"):
        return False
    if session.get("expires_at") and session["expires_at"] < datetime.utcnow():
        return False
    return True


class OTPManager:
    """
    Central OTP controller
    """

    @staticmethod
    def push_otp(session_id: str, otp_code: str):
        """
        Store OTP when received from watcher
        """
        session = get_session(session_id)
        if not session:
            return False

        if not is_session_valid(session):
            return False

        store_otp(
            session_id=session_id,
            user_id=session["user_id"],
            otp_code=otp_code
        )
        return True

    @staticmethod
    def fetch_otp(session_id: str):
        """
        Fetch latest valid OTP
        """
        return get_latest_otp(session_id)

    @staticmethod
    def consume_otp(otp):
        """
        Mark OTP as used (optional but recommended)
        """
        if not otp:
            return False

        mark_otp_used(otp["_id"])
        return True

    @staticmethod
    def can_view_otp(session: dict) -> bool:
        """
        Final gate before showing OTP to user
        """
        if not session:
            return False

        if not is_session_valid(session):
            return False

        return True