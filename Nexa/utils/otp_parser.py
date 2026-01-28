import re


OTP_PATTERNS = [
    r"\b(\d{5})\b",
    r"\b(\d{6})\b",
    r"login code[:\s]+(\d+)",
    r"code[:\s]+(\d+)"
]


def extract_otp(text: str) -> str | None:
    if not text:
        return None

    text = text.lower()

    for pattern in OTP_PATTERNS:
        match = re.search(pattern, text)
        if match:
            return match.group(1)

    return None