from __future__ import annotations
import os
from base64 import urlsafe_b64encode
from typing import Tuple

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a URL-safe base64 key from the given password and salt using PBKDF2.
    Returns: bytes suitable for use with Fernet.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend(),
    )
    key = kdf.derive(password.encode('utf-8'))
    return urlsafe_b64encode(key)


def new_salt() -> bytes:
    return os.urandom(16)


def encrypt(data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)


def decrypt(token: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(token)
