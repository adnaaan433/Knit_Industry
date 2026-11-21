"""Password hashing and constant-time verification using PBKDF2-HMAC-SHA256."""

import hashlib
import hmac
import os

ITERATIONS = 200_000
SALT_BYTES = 16
ALGO_PREFIX = "pbkdf2"


def hash_password(password: str, salt: bytes = None, iterations: int = ITERATIONS) -> str:
    """Hash a password with PBKDF2-HMAC-SHA256 and return 'pbkdf2$<iterations>$<salt_hex>$<hash_hex>'."""
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string.")
    if salt is None:
        salt = os.urandom(SALT_BYTES)
    elif isinstance(salt, str):
        salt = bytes.fromhex(salt)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, int(iterations))
    return f"{ALGO_PREFIX}${int(iterations)}${salt.hex()}${dk.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """Verify a password against a stored PBKDF2 hash in constant time."""
    if not isinstance(password, str) or not isinstance(stored, str):
        return False
    parts = stored.strip().split("$")
    if len(parts) != 4 or parts[0] != ALGO_PREFIX:
        return False
    try:
        iterations = int(parts[1])
        salt = bytes.fromhex(parts[2])
        expected_hash = bytes.fromhex(parts[3])
    except (ValueError, TypeError):
        return False
    if iterations < 1 or not salt or not expected_hash:
        return False
    candidate_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(candidate_hash, expected_hash)
