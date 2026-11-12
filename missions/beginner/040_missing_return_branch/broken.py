# Mission 040 - Cold Storage Returns None
# Work out when each backup tier may be deleted.
import datetime


def retention_days(tier):
    if tier == "hot":
        return 7
    elif tier == "warm":
        return 30
    elif tier == "cold":
        days = 365
    else:
        raise ValueError(f"unknown tier: {tier}")


def expiry_date(tier, created):
    return created + datetime.timedelta(days=retention_days(tier))
