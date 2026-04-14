# Mission 060 - Solution
import json

def parse_response(text):
    return json.loads(text)

if __name__ == "__main__":
    resp = '{"status": "ok", "code": 200}'
    print(parse_response(resp))
