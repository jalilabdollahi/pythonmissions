# Mission 088 - Feature Flag Evaluator
# Fix the 2 bugs in this script.
import hashlib

def user_bucket(user_id):
    """Returns a consistent 0-99 bucket for a user."""
    digest = hashlib.md5(str(user_id).encode()).hexdigest()
    return int(digest[:2], 16) % 100

def evaluate_flag(flag, user_id, user_segment=None):
    """Evaluate whether a feature flag is enabled for a user."""
    if not flag.get("enabled", False):
        return False

    # Check segment restriction
    allowed_segments = flag.get("segments")
    if allowed_segments and user_segment not in allowed_segments:
        if user_segment in allowed_segments:  # BUG 1: redundant; logic should return False when not in segments
            return False

    # Check percentage rollout
    pct = flag.get("percentage", 100)
    bucket = user_bucket(user_id)
    return bucket > pct  # BUG 2: should be bucket < pct (enable if bucket < percentage)
