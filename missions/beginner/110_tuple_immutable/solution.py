# Mission 110 - Solution
def add_to_config(config_tuple, item):
    return config_tuple + (item,)

if __name__ == "__main__":
    cfg = ("host=localhost", "port=5432")
    print(add_to_config(cfg, "db=myapp"))
