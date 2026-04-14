# Mission 029 - Solution

def unique_ips(ip_list):
    return list(set(ip_list))

if __name__ == "__main__":
    ips = ["10.0.0.1", "10.0.0.2", "10.0.0.1", "10.0.0.3", "10.0.0.2"]
    print(unique_ips(ips))
