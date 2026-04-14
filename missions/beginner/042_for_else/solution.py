# Mission 042 - Solution

def find_service(registry, name):
    for svc in registry:
        if svc["name"] == name:
            print(f"Found: {svc}")
            break
    else:
        print("not found")

if __name__ == "__main__":
    registry = [
        {"name": "web", "port": 80},
        {"name": "api", "port": 8080},
    ]
    find_service(registry, "api")
