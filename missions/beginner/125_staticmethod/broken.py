# Mission 125 - Validate IP Without Instance
import re

class NetworkUtil:
    IP_RE = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

    @classmethod
    def validate_ip(cls, ip):
        """Return True if ip matches basic IPv4 format."""
        return bool(NetworkUtil.IP_RE.match(ip))

if __name__ == "__main__":
    print(NetworkUtil.validate_ip("10.0.0.1"))
    print(NetworkUtil.validate_ip("not-an-ip"))
