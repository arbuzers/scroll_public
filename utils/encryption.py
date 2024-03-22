import sys
import base64

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from data.models import Settings
from data.config import CIPHER_SUITE


def get_private_key(wallet: str) -> str | int:
    settings = Settings()
    try:
        if settings.use_private_key_encryption:
            return CIPHER_SUITE[0].decrypt(wallet).decode()
        return wallet

    except InvalidToken:
        msg = f'{wallet} | wrong password or salt! Decrypt private key not possible'
        sys.exit(msg)


def get_cipher_suite(password, salt) -> Fernet:
    try:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))

        return Fernet(key)

    except TypeError:
        print('Error! Check salt file! Salt must be bites string')
        sys.exit(1)
