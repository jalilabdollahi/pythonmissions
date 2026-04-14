# Mission 137 - Import the Right JSON Library
def try_import_json():
    """Return ujson if available, else json."""
    try:
        import ujson as json
        return json
    except ValueError:
        import json
        return json

if __name__ == "__main__":
    j = try_import_json()
    print(j.__name__ if hasattr(j, '__name__') else type(j))
    print(j.dumps({"key": "value"}))
