# Mission 044 - Timeout and Retries Swapped
# Probe service endpoints with the agreed retry and timeout policy.


def run_probe(url, opener, retries=1, timeout=5):
    for _ in range(retries):
        try:
            opener(url, timeout)
            return True
        except ConnectionError:
            continue
    return False


def check_registry(url, opener):
    return run_probe(url, opener, 30, 3)


def check_database(url, opener):
    return run_probe(url, opener, 10, 2)
