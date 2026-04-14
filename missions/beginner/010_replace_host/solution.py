# Mission 010 - Solution

def swap_host(text, old, new):
    return text.replace(old, new)

if __name__ == "__main__":
    cfg = "host=server-01.internal"
    print(swap_host(cfg, "server-01", "server-02"))
