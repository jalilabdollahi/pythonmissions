# Mission 137 - Solution
def try_import_json():
    try:
        import ujson as json
        return json
    except ImportError:
        import json
        return json

if __name__ == "__main__":
    j = try_import_json()
    print(j.dumps({"key": "value"}))
