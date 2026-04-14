# Mission 125 - Solution
import re

class NetworkUtil:
    IP_RE = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

    @staticmethod
    def validate_ip(ip):
        return bool(NetworkUtil.IP_RE.match(ip))

if __name__ == "__main__":
    print(NetworkUtil.validate_ip("10.0.0.1"))
    print(NetworkUtil.validate_ip("not-an-ip"))
