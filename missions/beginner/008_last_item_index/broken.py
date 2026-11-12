# Mission 008 - Newest Backup
# Picks the newest backup from an oldest-first list.
def newest_backup(backups):
    return backups[len(backups)]


def oldest_backup(backups):
    return backups[0] if backups else None


def restore_plan(backups):
    newest = newest_backup(backups)
    if newest is None:
        return "no backups available"
    return f"restore from {newest}"


if __name__ == "__main__":
    print(restore_plan(["db-01.tar", "db-02.tar", "db-03.tar"]))
