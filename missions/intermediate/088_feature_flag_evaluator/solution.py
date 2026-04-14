# Mission 088 - Feature Flag Evaluator
# Fixed solution
import hashlib

def user_bucket(user_id):
    digest = hashlib.md5(str(user_id).encode()).hexdigest()
    return int(digest[:2], 16) % 100

def evaluate_flag(flag, user_id, user_segment=None):
    if not flag.get("enabled", False):
        return False

    allowed_segments = flag.get("segments")
    if allowed_segments and user_segment not in allowed_segments:
        return False

    pct = flag.get("percentage", 100)
    bucket = user_bucket(user_id)
    return bucket < pct
