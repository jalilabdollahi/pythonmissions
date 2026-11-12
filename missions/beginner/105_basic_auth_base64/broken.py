# Mission 105 - Registry Login Header
# Builds an HTTP Basic auth header for an internal artifact registry.
import base64


def basic_auth_header(user, password):
    credentials = f"{user}:{password}"
    token = base64.b64encode(credentials)
    return "Basic " + token


def read_basic_auth(header):
    scheme, _, token = header.partition(" ")
    if scheme != "Basic" or not token:
        raise ValueError("not a Basic authorization header")
    decoded = base64.b64decode(token).decode("utf-8")
    user, _, password = decoded.partition(":")
    return user, password


def registry_headers(user, password):
    return {
        "Authorization": basic_auth_header(user, password),
        "Accept": "application/json",
    }


if __name__ == "__main__":
    print(registry_headers("ci-bot", "s3cret")["Authorization"])
