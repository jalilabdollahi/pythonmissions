# Mission 011 - Solution

def find_port_offset(line):
    return line.find("port")

if __name__ == "__main__":
    print(find_port_offset("service port=8080"))
    print(find_port_offset("service name=web"))
