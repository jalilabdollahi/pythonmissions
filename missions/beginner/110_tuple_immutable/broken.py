# Mission 110 - Protect the Config Tuple
def add_to_config(config_tuple, item):
    """Return new tuple with item appended."""
    config_tuple.append(item)
    return config_tuple

if __name__ == "__main__":
    cfg = ("host=localhost", "port=5432")
    print(add_to_config(cfg, "db=myapp"))
