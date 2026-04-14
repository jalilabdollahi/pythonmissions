# Mission 060 - Parse the JSON Response
import json

def parse_response(text):
    """Parse JSON string and return dict."""
    return json.load(text)

if __name__ == "__main__":
    resp = '{"status": "ok", "code": 200}'
    print(parse_response(resp))
