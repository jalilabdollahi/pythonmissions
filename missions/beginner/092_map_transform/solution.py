# Mission 092 - Solution
def int_ports(port_strings):
    return list(map(int, port_strings))

if __name__ == "__main__":
    ports = ["80", "443", "8080", "5432"]
    result = int_ports(ports)
    print(type(result), result)
