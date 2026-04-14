# Mission 079 - Structured JSON Logging
# Fix the 2 bugs in this script.
import json
import sys
from datetime import datetime

def log_event(level, message, **extra):
    record = {
        "lvl": level,       # BUG 1: should be "level" not "lvl"
        "msg": message,
        "extra": extra,
    }
    # BUG 2: missing "timestamp" field
    line = json.dumps(record)
    sys.stdout.write(line + "\n")
    return record

def log_info(message, **extra):
    return log_event("INFO", message, **extra)

def log_error(message, **extra):
    return log_event("ERROR", message, **extra)
