# Mission 01 - Solution

server_name = "prod-web-01"
port = 8080
environment = "production"


def get_server_info():
    return {
        "server": server_name,
        "port": port,
        "env": environment,
    }


def main():
    print(f"Server: {server_name}")
    print(f"Port: {port}")
    print(f"Environment: {environment}")


if __name__ == "__main__":
    main()
