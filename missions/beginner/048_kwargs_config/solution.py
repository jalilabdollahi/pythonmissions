# Mission 048 - Solution

def build_config(**kwargs):
    return kwargs

if __name__ == "__main__":
    cfg = build_config(host="localhost", port=5432, debug=True)
    print(cfg)
