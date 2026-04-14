# Mission 061 - Solution
def get_port(env_val):
    return int(env_val)

if __name__ == "__main__":
    port = get_port("8080")
    print(type(port), port)
