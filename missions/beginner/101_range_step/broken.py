# Mission 101 - Generate Even Port Numbers
def even_ports(start, stop):
    """Return list of even port numbers from start to stop (exclusive)."""
    return list(range(start, stop, 1))

if __name__ == "__main__":
    print(even_ports(8000, 8010))
