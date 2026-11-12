# Mission 096 - Validator Without an Instance
# Request validation helpers grouped in a class.
import re

HOST_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")


class RequestValidator:
    def is_valid_port(port):
        return isinstance(port, int) and 1 <= port <= 65535

    def is_valid_hostname(name):
        return bool(HOST_PATTERN.match(name))

    def validate(self, request):
        problems = []
        if not self.is_valid_hostname(request.get("host", "")):
            problems.append("bad host")
        if not self.is_valid_port(request.get("port")):
            problems.append("bad port")
        return problems


def approve(requests):
    validator = RequestValidator()
    return [r for r in requests if not validator.validate(r)]


if __name__ == "__main__":
    batch = [{"host": "db-1", "port": 5432}, {"host": "-bad", "port": 0}]
    print(approve(batch))
