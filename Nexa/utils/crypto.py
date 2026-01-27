from cryptography.fernet import Fernet
import config

# IMPORTANT:
# SESSION_SECRET_KEY must be generated ONCE and stored permanently
fernet = Fernet(config.SESSION_SECRET_KEY)


def encrypt_text(value: str) -> str:
    if not value:
        return value
    return fernet.encrypt(value.encode()).decode()


def decrypt_text(value: str) -> str:
    if not value:
        return value
    return fernet.decrypt(value.encode()).decode()