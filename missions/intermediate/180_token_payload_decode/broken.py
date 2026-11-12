# Mission 180 - Unwrap The Token
# Decode the payload section of a JWT-like token and check its expiry.
import base64
import json


def decode_segment(segment):
    padded = segment
    return base64.b64decode(padded.encode("ascii"), validate=True)


def read_payload(token):
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("malformed token")
    return json.loads(decode_segment(parts[1]).decode("utf-8"))


def is_expired(token, now):
    exp = read_payload(token).get("exp")
    if exp is None:
        return False
    return now > exp


def describe(token):
    claims = read_payload(token)
    return "%s (%s)" % (claims.get("user", "?"), claims.get("scope", "no scope"))


def main(argv=None):
    import sys

    args = sys.argv[1:] if argv is None else argv
    for token in args:
        try:
            print(describe(token))
        except ValueError as exc:
            print("invalid token: %s" % exc)


if __name__ == "__main__":
    main()
