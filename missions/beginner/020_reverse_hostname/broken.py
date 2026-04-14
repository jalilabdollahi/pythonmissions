# Mission 020 - Reverse the Hostname
# Fix the bug.

def reverse_host(s):
    """Return the string reversed."""
    return s[::1]

if __name__ == "__main__":
    print(reverse_host("web.internal.net"))
