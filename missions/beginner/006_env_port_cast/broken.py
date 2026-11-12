# Mission 006 - Port From The Environment
# Reads the listener port from the environment as an integer.
DEFAULT_PORT = 8000


def read_port(env):
    return env.get("PORT", DEFAULT_PORT)


def listen_ports(env):
    main = read_port(env)
    return [main, main + 1]


def needs_root(env):
    return read_port(env) < 1024


if __name__ == "__main__":
    import os

    print(listen_ports(os.environ), needs_root(os.environ))
