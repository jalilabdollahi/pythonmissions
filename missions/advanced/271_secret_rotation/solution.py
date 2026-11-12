# Mission 271 - Gullwing Key Rotation (solution)
# Signing-key store that supports zero-downtime rotation with an overlap (grace) window.
import hashlib
import hmac
import math


class Key:
    def __init__(self, key_id, secret, activate_at):
        self.key_id = key_id
        self.secret = secret
        self.activate_at = activate_at


class KeyStore:
    """Keys sign from `activate_at` until a newer key activates, and keep verifying for
    `grace` more seconds so in-flight signatures do not break during a rotation."""

    def __init__(self, grace=3600):
        self.grace = grace
        self.keys = []
        self.revoked = set()

    def add(self, key_id, secret, activate_at):
        self.keys.append(Key(key_id, secret, activate_at))
        self.keys.sort(key=lambda k: k.activate_at)

    def revoke(self, key_id):
        self.revoked.add(key_id)

    def get(self, key_id):
        for key in self.keys:
            if key.key_id == key_id:
                return key
        return None

    def retire_at(self, key):
        index = self.keys.index(key)
        if index == len(self.keys) - 1:
            return math.inf
        return self.keys[index + 1].activate_at + self.grace

    def can_verify(self, key, now):
        if key.key_id in self.revoked:
            return False
        if now < key.activate_at:
            return False
        return now < self.retire_at(key)

    def signing_key(self, now):
        active = [k for k in self.keys if k.activate_at <= now and k.key_id not in self.revoked]
        if not active:
            raise LookupError("no usable signing key")
        return active[-1]

    def status(self, key, now):
        if key.key_id in self.revoked:
            return "revoked"
        if now < key.activate_at:
            return "pending"
        if now >= self.retire_at(key):
            return "retired"
        return "active" if key is self.signing_key(now) else "retiring"


def _mac(secret, payload):
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


def sign(store, payload, now):
    key = store.signing_key(now)
    return key.key_id, _mac(key.secret, payload)


def verify(store, payload, key_id, signature, now):
    key = store.get(key_id)
    if key is None or not store.can_verify(key, now):
        return False
    return hmac.compare_digest(_mac(key.secret, payload), signature)


def rotation_report(store, now):
    return {k.key_id: store.status(k, now) for k in store.keys}


if __name__ == "__main__":
    ks = KeyStore(grace=600)
    ks.add("k1", "alpha", 0)
    ks.add("k2", "beta", 1000)
    print(rotation_report(ks, 1200))
