# Mission 061 - Convert the Port String
def get_port(env_val):
    """Convert environment variable string to integer port."""
    return env_val

if __name__ == "__main__":
    port = get_port("8080")
    print(type(port), port)
