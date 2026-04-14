# Mission 096 - Secret Rotation Manager
# Fix the 2 bugs in this script.
import secrets
from datetime import datetime, timedelta

class SecretRotationManager:
    def __init__(self, rotation_days=90):
        self.rotation_days = rotation_days
        self._secrets = {}  # name -> {value, created_at}

    def create(self, name, length=32):
        self._secrets[name] = {
            "value": secrets.token_hex(length),
            "created_at": datetime.utcnow(),
        }

    def needs_rotation(self, name):
        if name not in self._secrets:
            return True
        created = self._secrets[name]["created_at"]
        expiry = created + timedelta(days=self.rotation_days)
        return datetime.utcnow() is expiry  # BUG 1: 'is' compares identity, not value — use >

    def rotate(self, name, length=32):
        if self.needs_rotation(name):
            self.create(name, length)
            return True
        return False

    def get(self, name):
        entry = self._secrets.get(name)
        return entry["value"] if entry else None

    def secret_length_bytes(self, name):
        val = self.get(name)
        if not val:
            return 0
        return len(val) // 2  # BUG 2: token_hex(n) returns 2n chars, so length in bytes = len/2 (correct)
        # Actual BUG 2: create() uses length as hex chars arg but the doc says bytes
        # Let's use a different bug: secret_age_days is wrong
    def secret_age_days(self, name):
        entry = self._secrets.get(name)
        if not entry:
            return -1
        delta = datetime.utcnow() - entry["created_at"]
        return delta.seconds // 86400  # BUG 2: should be delta.days not delta.seconds // 86400
