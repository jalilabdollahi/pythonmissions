# Mission 079 - Structured JSON Logging
# Fixed solution
import json
import sys
from datetime import datetime

def log_event(level, message, **extra):
    record = {
        "level": level,
        "msg": message,
        "timestamp": datetime.utcnow().isoformat(),
        **extra,
    }
    line = json.dumps(record)
    sys.stdout.write(line + "\n")
    return record

def log_info(message, **extra):
    return log_event("INFO", message, **extra)

def log_error(message, **extra):
    return log_event("ERROR", message, **extra)
