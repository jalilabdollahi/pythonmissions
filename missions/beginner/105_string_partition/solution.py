# Mission 105 - Solution
def split_host_port(endpoint):
    host, _, port = endpoint.partition(":")
    return host, port

if __name__ == "__main__":
    print(split_host_port("localhost:8080"))
