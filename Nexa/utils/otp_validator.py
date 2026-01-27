from datetime import datetime


def is_session_valid(session: dict) -> bool:
    if not session:
        return False

    if not session.get("active", False):
        return False

    if session.get("revoked", False):
        return False

    expires_at = session.get("expires_at")
    if expires_at and datetime.utcnow() > expires_at:
        return False

    return True


def is_otp_valid(otp: dict) -> bool:
    if not otp:
        return False

    if otp.get("status") != "unused":
        return False

    expires_at = otp.get("expires_at")
    if expires_at and datetime.utcnow() > expires_at:
        return False

    return True