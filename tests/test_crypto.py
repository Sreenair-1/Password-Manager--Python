import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so tests can import top-level modules
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from crypto_utils import derive_key, new_salt, encrypt, decrypt


def test_encrypt_decrypt():
    password = "master_secret"
    salt = new_salt()
    key = derive_key(password, salt)
    plaintext = b"supersecret"
    token = encrypt(plaintext, key)
    assert token != plaintext
    out = decrypt(token, key)
    assert out == plaintext


def test_key_different_with_different_salt():
    password = "master_secret"
    salt1 = new_salt()
    salt2 = new_salt()
    assert salt1 != salt2
    key1 = derive_key(password, salt1)
    key2 = derive_key(password, salt2)
    assert key1 != key2
