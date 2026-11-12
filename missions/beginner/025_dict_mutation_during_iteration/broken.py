# Mission 025 - Expired Sessions Sweep
# Removes expired sessions from an in-memory store.
def purge_expired(sessions, now):
    removed = 0
    for token, expires_at in sessions.items():
        if expires_at <= now:
            del sessions[token]
            removed += 1
    return removed


def active_tokens(sessions, now):
    return sorted(token for token, expires_at in sessions.items() if expires_at > now)


if __name__ == "__main__":
    store = {"tok-a": 100, "tok-b": 500, "tok-c": 90}
    print(purge_expired(store, 200), store)
