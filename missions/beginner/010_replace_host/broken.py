# Mission 010 - Replace the Hostname
# Fix the bug.

def swap_host(text, old, new):
    """Replace old hostname with new hostname in text."""
    return text.replace(new, old)

if __name__ == "__main__":
    cfg = "host=server-01.internal"
    print(swap_host(cfg, "server-01", "server-02"))
