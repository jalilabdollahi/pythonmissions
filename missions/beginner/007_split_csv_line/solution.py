# Mission 007 - Solution

def parse_field(line, index):
    parts = line.split(",")
    return parts[index].strip()

if __name__ == "__main__":
    line = "prod,web-01,8080,us-east-1"
    print(parse_field(line, 2))
