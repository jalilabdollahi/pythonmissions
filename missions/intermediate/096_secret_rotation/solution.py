# Mission 096 - Secret Rotation Manager
# Fixed solution
import secrets
from datetime import datetime, timedelta

class SecretRotationManager:
    def __init__(self, rotation_days=90):
        self.rotation_days = rotation_days
        self._secrets = {}

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
        return datetime.utcnow() > expiry

    def rotate(self, name, length=32):
        if self.needs_rotation(name):
            self.create(name, length)
            return True
        return False

    def get(self, name):
        entry = self._secrets.get(name)
        return entry["value"] if entry else None

    def secret_age_days(self, name):
        entry = self._secrets.get(name)
        if not entry:
            return -1
        delta = datetime.utcnow() - entry["created_at"]
        return delta.days
