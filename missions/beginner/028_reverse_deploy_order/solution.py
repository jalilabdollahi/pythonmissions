# Mission 028 - Solution

def reversed_order(steps):
    return steps[::-1]

if __name__ == "__main__":
    deploy = ["db-migrate", "backend", "frontend"]
    print(reversed_order(deploy))
