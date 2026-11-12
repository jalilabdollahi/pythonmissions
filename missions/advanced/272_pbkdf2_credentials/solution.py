# Mission 272 - Dockside Password Vault (solution)
# Password hashing with PBKDF2: random salts, stored work factor, constant-time comparison.
import base64
import hashlib
import hmac
import os

ALGORITHM = "pbkdf2_sha256"
CURRENT_ITERATIONS = 120_000
SALT_BYTES = 16


def _derive(password, salt, iterations):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)


def hash_password(password, salt=None, iterations=CURRENT_ITERATIONS):
    """Return `algorithm$iterations$salt_b64$hash_b64`."""
    if salt is None:
        salt = os.urandom(SALT_BYTES)
    digest = _derive(password, salt, iterations)
    return "$".join(
        [
            ALGORITHM,
            str(iterations),
            base64.b64encode(salt).decode("ascii"),
            base64.b64encode(digest).decode("ascii"),
        ]
    )


def parse(stored):
    """Split a stored hash into (iterations, salt, digest) or return None if malformed."""
    try:
        algorithm, iterations, salt_b64, digest_b64 = stored.split("$")
        if algorithm != ALGORITHM:
            return None
        count = int(iterations)
        if count <= 0:
            return None
        return count, base64.b64decode(salt_b64, validate=True), base64.b64decode(digest_b64, validate=True)
    except (ValueError, AttributeError):
        return None


def verify_password(password, stored):
    parsed = parse(stored)
    if parsed is None:
        return False
    iterations, salt, expected = parsed
    actual = _derive(password, salt, iterations)
    return hmac.compare_digest(actual, expected)


def needs_rehash(stored, target=CURRENT_ITERATIONS):
    parsed = parse(stored)
    if parsed is None:
        return True
    return parsed[0] < target


def login(stored, password, target=CURRENT_ITERATIONS):
    """Verify a login and transparently upgrade weak hashes.

    Returns (ok, replacement_hash). replacement_hash is None when nothing changed.
    """
    if not verify_password(password, stored):
        return False, None
    if needs_rehash(stored, target):
        return True, hash_password(password, iterations=target)
    return True, None


def policy_report(hashes, target=CURRENT_ITERATIONS):
    """hashes: username -> stored string. Returns usernames that need attention."""
    return sorted(name for name, stored in hashes.items() if needs_rehash(stored, target))


if __name__ == "__main__":
    stored = hash_password("correct horse battery staple", iterations=1000)
    print(verify_password("correct horse battery staple", stored), needs_rehash(stored))
