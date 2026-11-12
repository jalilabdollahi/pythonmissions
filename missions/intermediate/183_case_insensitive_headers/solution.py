# Mission 183 - Header Soup (solution)
# A small case-insensitive, multi-value HTTP header collection.
class Headers:
    def __init__(self, pairs=()):
        self._values = {}
        self._names = {}
        for name, value in pairs:
            self.add(name, value)

    def add(self, name, value):
        key = name.lower()
        self._names.setdefault(key, name)
        self._values.setdefault(key, []).append(value.strip())

    def get(self, name, default=None):
        values = self._values.get(name.lower())
        return ", ".join(values) if values else default

    def get_all(self, name):
        return list(self._values.get(name.lower(), []))

    def __contains__(self, name):
        return name.lower() in self._values

    def __len__(self):
        return len(self._values)

    def items(self):
        return [(self._names[key], ", ".join(vals)) for key, vals in self._values.items()]


def forward_lines(headers):
    return ["%s: %s" % (name, value) for name, value in headers.items()]


def main():
    headers = Headers([("Accept", "text/html"), ("accept", "application/json"), ("Host", "api.local")])
    for line in forward_lines(headers):
        print(line)
    print("has host:", "HOST" in headers)


if __name__ == "__main__":
    main()
