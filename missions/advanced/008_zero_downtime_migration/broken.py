# Mission 008 (Advanced) - Zero-Downtime Migration
# Fix the 2 bugs in this script.

class MigrationManager:
    PHASE_OLD = "old_only"
    PHASE_DUAL = "dual_write"
    PHASE_NEW = "new_only"

    def __init__(self, db):
        self.db = db  # dict simulating DB
        self.phase = self.PHASE_OLD

    def write_user(self, user_id, email, new_email_format):
        if self.phase == self.PHASE_OLD:
            self.db[user_id] = {"email": email}
        elif self.phase == self.PHASE_DUAL:
            self.db[user_id] = {"email": email}  # BUG 1: must also write new_email_format
        elif self.phase == self.PHASE_NEW:
            self.db[user_id] = {"email_v2": new_email_format}

    def read_user(self, user_id):
        record = self.db.get(user_id, {})
        if self.phase == self.PHASE_NEW:
            return record.get("email_v2")
        return record.get("email")

    def backfill(self):
        """Copy email -> email_v2 for records missing email_v2."""
        for uid, record in self.db.items():
            if "email_v2" not in record:
                self.db[uid]["email_v2"] = record.get("email", "").lower()
        # BUG 2: should only advance phase AFTER backfill completes; phase advance is missing

    def advance_phase(self):
        phases = [self.PHASE_OLD, self.PHASE_DUAL, self.PHASE_NEW]
        idx = phases.index(self.phase)
        if idx < len(phases) - 1:
            self.phase = phases[idx + 1]
